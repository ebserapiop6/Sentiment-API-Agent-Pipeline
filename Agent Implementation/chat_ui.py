"""
Streamlit Chat Interface for Customer Support Agent
Simple UI to test the agent workflow
"""
import streamlit as st
import sys
import os
from agent import SupportAgent, AgentInput

# Page config
st.set_page_config(
    page_title="AI Support Agent",
    page_icon="🤖",
    layout="wide"
)

# Initialize agent
@st.cache_resource
def get_agent():
    return SupportAgent()

agent = get_agent()

# Session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "sample_message" not in st.session_state:
    st.session_state.sample_message = None

# Sidebar - Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.subheader("API Status")
    sentiment_api = os.getenv("SENTIMENT_API_URL", "http://localhost:8000")
    
    # Check if agent has Groq client initialized (includes hardcoded key)
    if agent.groq_client is not None:
        st.success("✅ Groq API Key configured")
        st.caption("LLM responses enabled (Llama 3.3 70B)")
    else:
        st.warning("⚠️ Groq API Key not set")
        st.info("Set GROQ_API_KEY environment variable to enable LLM responses")
    
    st.text(f"Sentiment API: {sentiment_api}")
    
    st.divider()
    
    st.subheader("Decision Thresholds")
    st.metric("Escalation", f"{agent.ESCALATION_THRESHOLD}%", help="Negative confidence > 70% triggers escalation")
    st.metric("Clarification", f"{agent.CLARIFICATION_THRESHOLD}%", help="Confidence < 60% triggers clarifying question")
    
    st.divider()
    
    st.subheader("Sample Messages")
    if st.button("😡 Angry Customer"):
        st.session_state.sample_message = "This is absolutely terrible! I've been waiting for 3 hours and nobody has helped me!"
        st.rerun()
    if st.button("😊 Happy Customer"):
        st.session_state.sample_message = "Thank you so much! The support team was amazing!"
        st.rerun()
    if st.button("🤔 Unclear Message"):
        st.session_state.sample_message = "hmm not sure about this thing"
        st.rerun()
    if st.button("😐 Neutral Request"):
        st.session_state.sample_message = "I need help with my account settings"
        st.rerun()
    
    if st.button("🔄 Clear Conversation"):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.rerun()

# Main interface
st.title("🤖 AI Customer Support Agent")
st.caption("Powered by Sentiment Analysis + Groq LLM")

# Show connection status
try:
    import requests
    response = requests.get("http://localhost:8000/health", timeout=2)
    if response.status_code == 200:
        st.success("✅ Connected to Sentiment API")
    else:
        st.error("❌ Sentiment API not responding correctly")
except:
    st.error("❌ Sentiment API not reachable at http://localhost:8000")
    st.info("💡 Start the API with: `cd Deployment && python app.py`")

st.divider()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show metadata for agent responses
        if message["role"] == "assistant" and "metadata" in message:
            with st.expander("📊 Decision Details"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    sentiment = message["metadata"].get("sentiment", "N/A")
                    st.metric("Sentiment", sentiment)
                with col2:
                    confidence = message["metadata"].get("confidence", 0)
                    st.metric("Confidence", f"{confidence:.1f}%")
                with col3:
                    action = message["metadata"].get("action", "N/A")
                    st.metric("Action", action.replace("_", " ").title())
                
                st.caption(f"**Reasoning:** {message['metadata'].get('reasoning', 'N/A')}")

# Handle sample message
if st.session_state.sample_message:
    prompt = st.session_state.sample_message
    st.session_state.sample_message = None
else:
    prompt = st.chat_input("Type your message...")

if prompt:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process with agent
    with st.chat_message("assistant"):
        with st.spinner("Analyzing sentiment and generating response..."):
            try:
                # Create agent input
                agent_input = AgentInput(
                    customer_message=prompt,
                    conversation_history=st.session_state.conversation_history,
                    customer_id="DEMO_USER"
                )
                
                # Process message
                result = agent.process_message(agent_input)
                
                # Display response with formatting
                st.markdown(f"**Agent Response:**")
                st.markdown(result.action.response)
                
                # Show decision details in a prominent box
                st.info(f"**🔍 Analysis:** {result.sentiment.model_output.upper()} sentiment detected with {result.sentiment.confidence_score:.1f}% confidence")
                
                with st.expander("📊 Full Decision Details", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Sentiment", result.sentiment.model_output.title(), 
                                 delta="Negative" if result.sentiment.model_output == "negative" else None)
                    with col2:
                        st.metric("Confidence", f"{result.sentiment.confidence_score:.1f}%")
                    with col3:
                        action_display = result.action.action.replace("_", " ").title()
                        st.metric("Action Taken", action_display)
                    
                    st.markdown(f"**🤔 Reasoning:** {result.action.reasoning}")
                    
                    # Show metadata
                    if result.action.metadata:
                        st.json(result.action.metadata)
                
                # Add to conversation history
                st.session_state.conversation_history.append({
                    "role": "user",
                    "content": prompt
                })
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": result.action.response
                })
                
                # Add assistant message to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result.action.response,
                    "metadata": {
                        "sentiment": result.sentiment.model_output,
                        "confidence": result.sentiment.confidence_score,
                        "action": result.action.action,
                        "reasoning": result.action.reasoning
                    }
                })
                
            except Exception as e:
                st.error(f"❌ Error processing message: {str(e)}")
                
                # Provide helpful debugging info
                with st.expander("🔧 Debugging Information"):
                    st.write("**Error Type:**", type(e).__name__)
                    st.write("**Error Message:**", str(e))
                    st.code(str(e))
                    
                    # Check API status
                    try:
                        import requests
                        resp = requests.get("http://localhost:8000/health", timeout=2)
                        st.write("**API Status:**", resp.status_code)
                        st.json(resp.json())
                    except Exception as api_error:
                        st.write("**API Connection Error:**", str(api_error))
                    
                    st.markdown("""
                    **Common Issues:**
                    - Make sure Sentiment API is running: `cd Deployment && python app.py`
                    - Check if http://localhost:8000/health is accessible
                    - Verify Groq API key is set correctly
                    """)

# Footer
st.divider()
st.caption("💡 Tip: Try different message types to see how the agent responds based on sentiment and confidence thresholds.")
