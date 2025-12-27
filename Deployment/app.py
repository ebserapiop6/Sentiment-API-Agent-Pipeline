#!/usr/bin/env python3
"""
FastAPI Sentiment Analysis Microservice
Production-ready REST API for sentiment prediction using trained SVM model.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sentiment Analysis API",
    description="Production-ready microservice for sentiment classification (positive/neutral/negative)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variables
MODEL = None
EMBEDDER = None
LABEL_MAP = None

# Model path
MODEL_PATH = os.getenv("MODEL_PATH", "../Sentiment model/results/model.joblib")


class PredictionRequest(BaseModel):
    """Request schema for single prediction"""
    text: str = Field(..., min_length=1, max_length=5000, example="I hate going to that restaurant")


class BatchPredictionRequest(BaseModel):
    """Request schema for batch predictions"""
    texts: List[str] = Field(..., min_items=1, max_items=100, example=["Great service!", "Terrible experience"])


class PredictionResponse(BaseModel):
    """Response schema for sentiment prediction"""
    model_output: str = Field(..., example="negative")
    confidence_score: float = Field(..., example=98.42)
    text: Optional[str] = Field(None, example="I hate going to that restaurant")


class BatchPredictionResponse(BaseModel):
    """Response schema for batch predictions"""
    predictions: List[PredictionResponse]
    count: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    timestamp: str
    version: str


def load_model():
    """Load trained model and embedder on startup"""
    global MODEL, EMBEDDER, LABEL_MAP
    
    try:
        logger.info(f"Loading model from {MODEL_PATH}")
        model_data = joblib.load(MODEL_PATH)
        
        MODEL = model_data['classifier']
        EMBEDDER = model_data['embedder']
        LABEL_MAP = model_data['idx2label']
        
        logger.info("Model loaded successfully")
        logger.info(f"Available labels: {list(LABEL_MAP.values())}")
        
    except FileNotFoundError:
        logger.error(f"Model file not found at {MODEL_PATH}")
        raise RuntimeError(f"Model file not found: {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise RuntimeError(f"Failed to load model: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Initialize model on application startup"""
    load_model()


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Sentiment Analysis API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/batch_predict",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy" if MODEL is not None else "unhealthy",
        model_loaded=MODEL is not None,
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_sentiment(request: PredictionRequest):
    """
    Predict sentiment for a single text input.
    
    Returns:
    - model_output: positive|neutral|negative
    - confidence_score: float (0-100, rounded to 2 decimals)
    - text: original input text
    """
    if MODEL is None or EMBEDDER is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        # Generate embedding
        embedding = EMBEDDER.encode([request.text], show_progress_bar=False, batch_size=1)
        
        # Predict
        prediction = MODEL.predict(embedding)[0]
        probabilities = MODEL.predict_proba(embedding)[0]
        
        # Get confidence score (percentage)
        confidence = round(float(probabilities[prediction]) * 100, 2)
        sentiment = LABEL_MAP[prediction]
        
        logger.info(f"Prediction: {sentiment} ({confidence}%) for text: {request.text[:50]}...")
        
        return PredictionResponse(
            model_output=sentiment,
            confidence_score=confidence,
            text=request.text
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/batch_predict", response_model=BatchPredictionResponse, tags=["Prediction"])
async def batch_predict_sentiment(request: BatchPredictionRequest):
    """
    Predict sentiment for multiple texts in batch.
    
    Supports up to 100 texts per request for efficient processing.
    """
    if MODEL is None or EMBEDDER is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        # Generate embeddings for all texts
        embeddings = EMBEDDER.encode(request.texts, show_progress_bar=False, batch_size=32)
        
        # Predict for all
        predictions = MODEL.predict(embeddings)
        probabilities = MODEL.predict_proba(embeddings)
        
        # Build response
        results = []
        for i, text in enumerate(request.texts):
            pred = predictions[i]
            conf = round(float(probabilities[i, pred]) * 100, 2)
            sentiment = LABEL_MAP[pred]
            
            results.append(PredictionResponse(
                model_output=sentiment,
                confidence_score=conf,
                text=text
            ))
        
        logger.info(f"Batch prediction completed: {len(results)} texts processed")
        
        return BatchPredictionResponse(
            predictions=results,
            count=len(results)
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/model/info", tags=["Model"])
async def model_info():
    """Get information about the loaded model"""
    if MODEL is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    return {
        "model_type": type(MODEL).__name__,
        "labels": list(LABEL_MAP.values()),
        "embedding_model": "all-MiniLM-L6-v2",
        "embedding_dimension": 384,
        "trained_accuracy": "87%"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
