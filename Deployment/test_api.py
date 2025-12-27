#!/usr/bin/env python3
"""
Test script for the Sentiment API
Demonstrates all available endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("\n" + "="*80)
    print("Testing Root Endpoint")
    print("="*80)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*80)
    print("Testing Health Check")
    print("="*80)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_single_prediction():
    """Test single prediction endpoint"""
    print("\n" + "="*80)
    print("Testing Single Prediction")
    print("="*80)
    
    test_cases = [
        "I hate going to that restaurant",
        "This is amazing! Best experience ever!",
        "It was okay, nothing special"
    ]
    
    for text in test_cases:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"text": text}
        )
        print(f"\nInput: {text}")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n" + "="*80)
    print("Testing Batch Prediction")
    print("="*80)
    
    texts = [
        "Great service!",
        "Terrible experience",
        "It was okay",
        "I love this product!",
        "Worst purchase ever"
    ]
    
    response = requests.post(
        f"{BASE_URL}/batch_predict",
        json={"texts": texts}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Processed: {result['count']} texts\n")
    for pred in result['predictions']:
        print(f"Text: {pred['text']}")
        print(f"  → {pred['model_output']} ({pred['confidence_score']}%)")

def test_model_info():
    """Test model info endpoint"""
    print("\n" + "="*80)
    print("Testing Model Info")
    print("="*80)
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("\n" + "="*80)
    print("SENTIMENT API TEST SUITE")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    
    try:
        test_root()
        test_health()
        test_model_info()
        test_single_prediction()
        test_batch_prediction()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETED")
        print("="*80)
        
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to API server")
        print("Make sure the server is running: python app.py")
    except Exception as e:
        print(f"\nERROR: {str(e)}")
