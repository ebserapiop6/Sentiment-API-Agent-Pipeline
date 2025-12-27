"""
Quick test to verify agent works correctly
"""
from agent import SupportAgent, AgentInput

# Initialize agent
agent = SupportAgent()

# Test case
test_message = "This is absolutely terrible! I've been waiting for 3 hours!"

print("="*80)
print("TESTING AGENT")
print("="*80)
print(f"\nInput: {test_message}")

# Create input
agent_input = AgentInput(
    customer_message=test_message,
    conversation_history=[],
    customer_id="TEST_USER"
)

# Process
try:
    result = agent.process_message(agent_input)
    
    print(f"\n✅ SUCCESS!")
    print(f"\n📊 SENTIMENT:")
    print(f"  - Type: {result.sentiment.model_output}")
    print(f"  - Confidence: {result.sentiment.confidence_score:.1f}%")
    
    print(f"\n🤖 ACTION:")
    print(f"  - Action: {result.action.action}")
    print(f"  - Reasoning: {result.action.reasoning}")
    
    print(f"\n💬 RESPONSE:")
    print(f"  {result.action.response}")
    
    print("\n" + "="*80)
    print("TEST PASSED - Agent is working correctly!")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nMake sure:")
    print("1. Sentiment API is running: cd ../Deployment && python app.py")
    print("2. API is accessible at: http://localhost:8000/health")
