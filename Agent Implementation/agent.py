"""
AI Agent for Customer Support Workflow
Uses Sentiment API + Groq LLM for intelligent support routing
"""
import os
import json
import requests
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from groq import Groq

# Configuration
SENTIMENT_API_URL = os.getenv("SENTIMENT_API_URL", "http://localhost:8000")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


# ============================================================================
# JSON SCHEMAS
# ============================================================================

class SentimentRequest(BaseModel):
    """Schema for sentiment analysis request"""
    text: str = Field(..., description="Customer message text")


class SentimentResponse(BaseModel):
    """Schema for sentiment analysis response"""
    model_output: Literal["positive", "neutral", "negative"]
    confidence_score: float = Field(..., ge=0, le=100)
    text: str


class AgentAction(BaseModel):
    """Schema for agent action decision"""
    action: Literal["escalate_to_support", "ask_clarifying_question", "provide_helpful_response", "acknowledge_feedback"]
    reasoning: str = Field(..., description="Explanation for the action")
    response: str = Field(..., description="Message to send to customer")
    metadata: Optional[Dict] = Field(default_factory=dict)


class AgentInput(BaseModel):
    """Schema for agent input"""
    customer_message: str = Field(..., description="The customer's message")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Previous messages")
    customer_id: Optional[str] = Field(None, description="Customer identifier")


class AgentOutput(BaseModel):
    """Schema for agent output"""
    sentiment: SentimentResponse
    action: AgentAction
    confidence: float = Field(..., description="Overall confidence in the decision")


# ============================================================================
# AGENT CORE LOGIC
# ============================================================================

class SupportAgent:
    """AI Agent for customer support workflow"""
    
    def __init__(self, sentiment_api_url: str = SENTIMENT_API_URL, groq_api_key: str = GROQ_API_KEY):
        self.sentiment_api_url = sentiment_api_url
        self.groq_api_key = groq_api_key
        self.groq_client = Groq(api_key=groq_api_key) if groq_api_key else None
        
        # Thresholds for decision making
        self.ESCALATION_THRESHOLD = 70.0  # Negative sentiment confidence > 70% → escalate
        self.CLARIFICATION_THRESHOLD = 60.0  # Low confidence < 60% → ask clarifying question
    
    def get_sentiment(self, text: str) -> SentimentResponse:
        """Call sentiment API to analyze customer message"""
        try:
            response = requests.post(
                f"{self.sentiment_api_url}/predict",
                json={"text": text},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return SentimentResponse(**data)
        except Exception as e:
            print(f"Error calling sentiment API: {e}")
            # Fallback: neutral sentiment with low confidence
            return SentimentResponse(
                model_output="neutral",
                confidence_score=50.0,
                text=text
            )
    
    def decide_action(self, sentiment: SentimentResponse, customer_message: str, conversation_history: List[Dict] = None) -> AgentAction:
        """Decide what action to take based on sentiment and context"""
        
        # Rule 1: High-confidence negative sentiment → Escalate
        if sentiment.model_output == "negative" and sentiment.confidence_score >= self.ESCALATION_THRESHOLD:
            return AgentAction(
                action="escalate_to_support",
                reasoning=f"Detected strong negative sentiment ({sentiment.confidence_score:.1f}% confidence). Customer needs immediate human assistance.",
                response="I understand you're experiencing difficulties. Let me connect you with a support specialist who can help resolve this right away.",
                metadata={"priority": "high", "sentiment": sentiment.model_output, "confidence": sentiment.confidence_score}
            )
        
        # Rule 2: Low confidence → Ask clarifying question
        if sentiment.confidence_score < self.CLARIFICATION_THRESHOLD:
            return AgentAction(
                action="ask_clarifying_question",
                reasoning=f"Sentiment unclear (confidence: {sentiment.confidence_score:.1f}%). Need more context to provide appropriate response.",
                response="I want to make sure I understand your concern correctly. Could you provide more details about what you're experiencing?",
                metadata={"needs_clarification": True, "confidence": sentiment.confidence_score}
            )
        
        # Rule 3: Moderate negative → Use LLM for empathetic response
        if sentiment.model_output == "negative":
            if self.groq_client:
                llm_response = self._generate_empathetic_response(customer_message, conversation_history)
                return AgentAction(
                    action="provide_helpful_response",
                    reasoning=f"Moderate negative sentiment ({sentiment.confidence_score:.1f}%). Providing empathetic assistance.",
                    response=llm_response,
                    metadata={"sentiment": sentiment.model_output, "confidence": sentiment.confidence_score}
                )
            else:
                return AgentAction(
                    action="provide_helpful_response",
                    reasoning=f"Moderate negative sentiment. Offering assistance.",
                    response="I'm sorry to hear you're having trouble. I'm here to help! Could you tell me more about the issue so I can assist you better?",
                    metadata={"sentiment": sentiment.model_output, "confidence": sentiment.confidence_score}
                )
        
        # Rule 4: Positive sentiment → Acknowledge and thank
        if sentiment.model_output == "positive":
            if self.groq_client:
                llm_response = self._generate_positive_response(customer_message)
                return AgentAction(
                    action="acknowledge_feedback",
                    reasoning=f"Positive sentiment detected ({sentiment.confidence_score:.1f}%). Acknowledging customer satisfaction.",
                    response=llm_response,
                    metadata={"sentiment": sentiment.model_output, "confidence": sentiment.confidence_score}
                )
            else:
                return AgentAction(
                    action="acknowledge_feedback",
                    reasoning=f"Positive sentiment. Thanking customer.",
                    response="Thank you for your positive feedback! We're glad we could help. Is there anything else I can assist you with?",
                    metadata={"sentiment": sentiment.model_output, "confidence": sentiment.confidence_score}
                )
        
        # Rule 5: Neutral sentiment → Provide helpful response
        if self.groq_client:
            llm_response = self._generate_helpful_response(customer_message, conversation_history)
            return AgentAction(
                action="provide_helpful_response",
                reasoning=f"Neutral sentiment ({sentiment.confidence_score:.1f}%). Providing informative response.",
                response=llm_response,
                metadata={"sentiment": sentiment.model_output, "confidence": sentiment.confidence_score}
            )
        else:
            return AgentAction(
                action="provide_helpful_response",
                reasoning=f"Neutral sentiment. Offering general assistance.",
                response="I'm here to help! How can I assist you today?",
                metadata={"sentiment": sentiment.model_output, "confidence": sentiment.confidence_score}
            )
    
    def _generate_empathetic_response(self, customer_message: str, conversation_history: List[Dict] = None) -> str:
        """Use Groq LLM to generate empathetic response for negative sentiment"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful customer support agent. The customer is experiencing frustration or dissatisfaction. Respond with empathy, acknowledge their concern, and offer assistance. Keep response under 100 words."
                }
            ]
            
            if conversation_history:
                for msg in conversation_history[-3:]:  # Last 3 messages for context
                    messages.append(msg)
            
            messages.append({
                "role": "user",
                "content": customer_message
            })
            
            completion = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "I understand your concern. Let me help you with that. Could you provide more details?"
    
    def _generate_positive_response(self, customer_message: str) -> str:
        """Use Groq LLM to generate response for positive sentiment"""
        try:
            completion = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a friendly customer support agent. The customer is happy or satisfied. Respond warmly, thank them, and ask if there's anything else you can help with. Keep response under 80 words."
                    },
                    {
                        "role": "user",
                        "content": customer_message
                    }
                ],
                temperature=0.7,
                max_tokens=120
            )
            
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "Thank you for your positive feedback! We're happy to help. Is there anything else I can assist you with?"
    
    def _generate_helpful_response(self, customer_message: str, conversation_history: List[Dict] = None) -> str:
        """Use Groq LLM to generate helpful response for neutral sentiment"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful customer support agent. Provide clear, informative assistance. Keep response under 100 words."
                }
            ]
            
            if conversation_history:
                for msg in conversation_history[-3:]:
                    messages.append(msg)
            
            messages.append({
                "role": "user",
                "content": customer_message
            })
            
            completion = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "I'm here to help! Could you provide more details about what you need assistance with?"
    
    def process_message(self, agent_input: AgentInput) -> AgentOutput:
        """Main processing pipeline"""
        # Step 1: Analyze sentiment
        sentiment = self.get_sentiment(agent_input.customer_message)
        
        # Step 2: Decide action based on sentiment + thresholds
        action = self.decide_action(
            sentiment,
            agent_input.customer_message,
            agent_input.conversation_history
        )
        
        # Step 3: Return structured output
        return AgentOutput(
            sentiment=sentiment,
            action=action,
            confidence=sentiment.confidence_score
        )


# ============================================================================
# SAMPLE PAYLOADS (for testing)
# ============================================================================

SAMPLE_INPUTS = {
    "escalation_case": {
        "customer_message": "This is absolutely terrible! I've been waiting for 3 hours and nobody has helped me. I want a refund NOW!",
        "conversation_history": [],
        "customer_id": "CUST001"
    },
    "clarification_case": {
        "customer_message": "hmm not sure about this thing",
        "conversation_history": [],
        "customer_id": "CUST002"
    },
    "positive_case": {
        "customer_message": "Thank you so much! The support team was amazing and solved my issue quickly.",
        "conversation_history": [],
        "customer_id": "CUST003"
    },
    "neutral_case": {
        "customer_message": "I need help with my account settings",
        "conversation_history": [],
        "customer_id": "CUST004"
    }
}


if __name__ == "__main__":
    # Example usage
    agent = SupportAgent()
    
    print("="*80)
    print("SUPPORT AGENT - SAMPLE RUNS")
    print("="*80)
    
    for case_name, input_data in SAMPLE_INPUTS.items():
        print(f"\n{'='*80}")
        print(f"Case: {case_name.upper()}")
        print(f"{'='*80}")
        print(f"Input: {input_data['customer_message']}")
        
        agent_input = AgentInput(**input_data)
        result = agent.process_message(agent_input)
        
        print(f"\n→ Sentiment: {result.sentiment.model_output} ({result.sentiment.confidence_score:.1f}%)")
        print(f"→ Action: {result.action.action}")
        print(f"→ Reasoning: {result.action.reasoning}")
        print(f"→ Response: {result.action.response}")
