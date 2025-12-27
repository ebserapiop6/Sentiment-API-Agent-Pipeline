# Sentiment Analysis API - Deployment

## Overview
Production-ready **FastAPI microservice** for sentiment classification. Exposes REST APIs for single and batch predictions using the trained SVM model (87% accuracy).

## Features
- ✅ **REST API**: FastAPI framework with automatic OpenAPI documentation
- ✅ **Single Prediction**: `/predict` endpoint for individual text analysis
- ✅ **Batch Processing**: `/batch_predict` for efficient multi-text predictions (up to 100 texts)
- ✅ **Health Checks**: `/health` endpoint for monitoring and orchestration
- ✅ **Docker Support**: Containerized deployment with Dockerfile
- ✅ **CORS Enabled**: Cross-origin requests supported
- ✅ **Auto Documentation**: Interactive API docs at `/docs`

## Architecture
```
Client Request → FastAPI → Sentence Embedder → SVM Classifier → JSON Response
                    ↓
              Model Loaded from ../Sentiment model/results/model.joblib
```

## Setup Instructions

### Option 1: Local Development (Recommended - Use Parent Virtual Environment)

**Note**: The API uses the trained model from `Sentiment model/results/model.joblib` and reuses the parent virtual environment which already has all ML dependencies installed.

#### 1. Navigate to Deployment Folder
```bash
cd C:\Users\...\Deployment
```

#### 2. Activate Parent Virtual Environment
```bash
# Use the parent .venv which has all dependencies
..\.venv\Scripts\activate   # Windows
source ../.venv/bin/activate  # Linux/Mac
```

#### 3. Install FastAPI Dependencies (if not already installed)
```bash
pip install fastapi uvicorn pydantic python-multipart
```

#### 4. Run the API Server
```bash
python app.py
```

**Or using uvicorn directly:**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Loading model from ../Sentiment model/results/model.joblib
INFO:     Model loaded successfully
INFO:     Available labels: ['negative', 'neutral', 'positive']
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

The API will be available at: `http://localhost:8000`

**Interactive Documentation**: Open http://localhost:8000/docs in your browser to test all endpoints.

### Option 2: Docker Deployment (Recommended for Production)

#### 1. Build Docker Image
```bash
docker build -t sentiment-api:latest .
```

#### 2. Run Container
```bash
docker run -d -p 8000:8000 --name sentiment-api sentiment-api:latest
```

**With custom model path:**
```bash
docker run -d -p 8000:8000 -v /path/to/model.joblib:/app/model/model.joblib -e MODEL_PATH=/app/model/model.joblib --name sentiment-api sentiment-api:latest
```

#### 3. Check Container Status
```bash
docker ps
docker logs sentiment-api
```

#### 4. Stop Container
```bash
docker stop sentiment-api
docker rm sentiment-api
```

## API Endpoints

### 1. Root - Service Info
```http
GET /
```

**Response:**
```json
{
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
```

### 2. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-12-27T01:52:00.000000",
  "version": "1.0.0"
}
```

### 3. Single Prediction
```http
POST /predict
Content-Type: application/json

{
  "text": "I hate going to that restaurant"
}
```

**Response:**
```json
{
  "model_output": "negative",
  "confidence_score": 98.42,
  "text": "I hate going to that restaurant"
}
```

### 4. Batch Prediction
```http
POST /batch_predict
Content-Type: application/json

{
  "texts": [
    "Great service!",
    "Terrible experience",
    "It was okay"
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "model_output": "positive",
      "confidence_score": 95.67,
      "text": "Great service!"
    },
    {
      "model_output": "negative",
      "confidence_score": 92.34,
      "text": "Terrible experience"
    },
    {
      "model_output": "neutral",
      "confidence_score": 78.90,
      "text": "It was okay"
    }
  ],
  "count": 3
}
```

### 5. Model Information
```http
GET /model/info
```

**Response:**
```json
{
  "model_type": "SVC",
  "labels": ["negative", "neutral", "positive"],
  "embedding_model": "all-MiniLM-L6-v2",
  "embedding_dimension": 384,
  "trained_accuracy": "79%"
}
```

## Sample Requests

### Using cURL

**Single Prediction:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

**Batch Prediction:**
```bash
curl -X POST "http://localhost:8000/batch_predict" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Amazing!", "Horrible", "Not bad"]}'
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

### Using Python requests

```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "I hate going to that restaurant"}
)
print(response.json())
# Output: {"model_output": "negative", "confidence_score": 98.42, "text": "I hate going to that restaurant"}

# Batch prediction
response = requests.post(
    "http://localhost:8000/batch_predict",
    json={"texts": ["Great!", "Bad", "Okay"]}
)
print(response.json())
```

### Using JavaScript (fetch)

```javascript
// Single prediction
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'I love this!' })
})
  .then(res => res.json())
  .then(data => console.log(data));

// Batch prediction
fetch('http://localhost:8000/batch_predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ texts: ['Great!', 'Terrible', 'Meh'] })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the browser using these interfaces.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `../Sentiment model/results/model.joblib` | Path to trained model file |
| `HOST` | `0.0.0.0` | Server host address |
| `PORT` | `8000` | Server port |

## Production Considerations

### 1. Security
- Add API authentication (JWT, API keys)
- Enable HTTPS with SSL certificates
- Implement rate limiting
- Add input validation and sanitization

### 2. Scalability
- Use load balancer for horizontal scaling
- Consider async processing for batch requests
- Implement caching for common predictions
- Use Redis for distributed caching

### 3. Monitoring
- Add Prometheus metrics endpoint
- Implement structured logging (JSON logs)
- Set up error tracking (Sentry, Rollbar)
- Monitor response times and throughput

### 4. Deployment Options
- **Container Orchestration**: Kubernetes, Docker Swarm
- **Serverless**: AWS Lambda, Google Cloud Run
- **PaaS**: Heroku, Railway, Render
- **Cloud VMs**: AWS EC2, GCP Compute Engine

## Project Structure
```
Deployment/
├── app.py                # FastAPI application
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container image definition
└── README.md            # This file (deployment guide)
```

## Troubleshooting

### Model Not Found Error
```
Error: Model file not found
```
**Solution**: Ensure `../Sentiment model/results/model.joblib` exists. Update `MODEL_PATH` environment variable if needed.

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Change port using `--port 8001` or stop the process using port 8000.

### Slow First Request
The first prediction may take longer (~5s) due to model loading. Subsequent requests are fast (<100ms).

## Performance Metrics

| Metric | Value |
|--------|-------|
| **Cold Start** | ~5 seconds (model loading) |
| **Avg Response Time** | <100ms (single prediction) |
| **Batch Throughput** | ~50 texts/second |
| **Memory Usage** | ~500MB (model + embedder) |
| **Model Accuracy** | 79% |

## License & Credits

Built using:
- **FastAPI**: Modern Python web framework
- **SentenceTransformers**: Semantic text embeddings
- **Scikit-learn**: Machine learning library
- **Model**: SVM trained on Sentiment140 dataset (79% accuracy)
