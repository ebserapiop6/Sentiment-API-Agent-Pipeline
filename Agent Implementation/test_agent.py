import requests
import json

AGENT_URL = "http://localhost:8000"

# Test cases
test_cases = [
    {
        "name": "Escalation Test",
        "text": "This is absolutely terrible! I've been waiting for 3 hours and nobody has helped me! I want a refund NOW!",
        "expected_sentiment": "negative",
        "expected_confidence": ">70%"
    },
    {
        "name": "Clarification Test", 
        "text": "hmm not sure about this thing",
        "expected_sentiment": "neutral",
        "expected_confidence": "<60%"
    },
    {
        "name": "Positive Test",
        "text": "Thank you so much! The support was amazing and resolved my issue quickly!",
        "expected_sentiment": "positive"
    },
    {
        "name": "Neutral Test",
        "text": "I need help with my account settings",
        "expected_sentiment": "neutral"
    }
]

print("="*80)
print("TESTING AGENT INTEGRATION")
print("="*80)

for test in test_cases:
    print(f"\n{test['name']}")
    print(f"Input: {test['text']}")
    
    # Call Sentiment API
    response = requests.post(
        f"{AGENT_URL}/predict",
        json={"text": test['text']}
    )
    
    result = response.json()
    print(f"→ Sentiment: {result['model_output']} ({result['confidence_score']:.1f}%)")
    print(f"→ Expected: {test['expected_sentiment']}")
    print("✅ PASS" if result['model_output'] == test['expected_sentiment'] else "⚠️ CHECK")

print("\n" + "="*80)
print("TESTING COMPLETE")
print("="*80)