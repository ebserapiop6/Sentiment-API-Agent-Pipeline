# Sprout AI Technical Task - Complete Solution

## Project Description

**End-to-end intelligent customer support system** combining machine learning sentiment analysis, REST API deployment, and AI agent automation.

### What This Project Does

This is a **production-ready AI customer support automation system** that:

1. **Analyzes customer sentiment** in real-time using a custom-trained ML model
2. **Exposes predictions via REST API** with FastAPI for easy integration
3. **Automates support workflows** using an intelligent agent powered by Groq's Llama 3.3 70B
4. **Routes messages intelligently** based on sentiment and confidence thresholds:
   - 😡 Angry customers → Escalated to human support
   - 🤔 Unclear messages → Asks clarifying questions
   - 😊 Happy customers → Acknowledges and thanks
   - 😐 General queries → Provides helpful information

### Key Highlights
- **Sentiment Classification Accuracy** using sentence embeddings + SVM with GridSearch optimization
- **<100ms API Response Time** with FastAPI microservice
- **LLM-Powered Agent** using Groq's Llama 3.3 70B for contextual responses
- **Interactive Chat UI** built with Streamlit
- **Production-Ready Deployment** with Docker support (Demoed through local)
- **Real-Time Decision Visualization** with confidence metrics for dev monitoring

### Features at a Glance

#### Machine Learning
- Custom sentiment classifier (negative/neutral/positive)
- Advanced feature engineering with sentence embeddings (384 dimensions)
- Hyperparameter grid search across 4 classifiers
- Confidence scores with every prediction (0-100%)

#### REST API
- 5 RESTful endpoints (predict, batch, health, info, root)
- Auto-generated OpenAPI/Swagger documentation
- Request validation with Pydantic schemas
- CORS support for cross-origin requests
- Batch prediction for multiple texts
- Docker containerization

#### AI Agent
- 4 intelligent action types (escalate, clarify, acknowledge, help)
- Groq LLM integration 
- Context-aware responses using conversation history
- Threshold-based decision making (70% escalation, 60% clarification)
- Real-time sentiment analysis
- Interactive Streamlit chat interface
- Sample message testing buttons
- Decision transparency with detailed reasoning

---

## Table of Contents

- [Quick Start](#-quick-start-3-minutes)
- [Project Structure](#-project-structure)
- [Commands Reference](#-commands-reference)
- [Testing](#-testing)
- [Key Results](#-key-results)
- [Documentation](#-documentation)

---

## Project Components

**Each component has its own detailed README with setup instructions and documentation.**

### 1. Sentiment Analysis Model ([`Sentiment model/`](Sentiment%20model/README.md))
Machine learning pipeline for text classification with 87% accuracy
- Sentence embeddings (all-MiniLM-L6-v2) + SVM classifier
- Hyperparameter optimization across 180 configurations
- Outputs predictions with confidence scores

### 2. Sentiment API Service ([`Deployment/`](Deployment/README.md))
Production REST API for real-time sentiment inference
- FastAPI with 5 endpoints + OpenAPI docs
- Docker support, <100ms response time
- Batch prediction capabilities

### 3. AI Agent Implementation ([`Agent Implementation/`](Agent%20Implementation/README.md))
Intelligent customer support automation with LLM
- 4 action types (escalate, clarify, acknowledge, help)
- Groq LLM (Llama 3.3 70B) integration
- Interactive Streamlit chat interface

---

## System Architecture

```
┌─────────────┐
│   Customer  │
│   Message   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│      Streamlit Chat Interface           │
│  (Agent Implementation/chat_ui.py)      │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│        Support Agent Logic              │
│    (Agent Implementation/agent.py)      │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  1. Call Sentiment API            │ │
│  │  2. Analyze confidence            │ │
│  │  3. Apply decision rules          │ │
│  │  4. Generate LLM response         │ │
│  └───────────────────────────────────┘ │
└──────┬────────────────────┬─────────────┘
       │                    │
       ▼                    ▼
┌──────────────┐    ┌──────────────────┐
│ Sentiment API│    │   Groq LLM API   │
│  (FastAPI)   │    │ Llama 3.3 70B    │
│              │    │                  │
│  Deployment/ │    │ Context-aware    │
│    app.py    │    │   responses      │
└──────┬───────┘    └──────────────────┘
       │
       ▼
┌──────────────────┐
│  ML Model        │
│  (SVM + Embedder)│
│                  │
│  87% Accuracy    │
│  model.joblib    │
└──────────────────┘
```

---

## Quick Start (3 Minutes)

### Prerequisites
- Python 3.10+
- Internet connection (for package installation)
- 2 terminal windows

### Step 1: Setup Environment (One-Time)
```bash
# Navigate to project
cd C:\Users\...

# Create virtual environment
python -m venv .venv

# Activate venv
.venv\Scripts\activate

# Install all dependencies
pip install sentence-transformers scikit-learn pandas numpy joblib fastapi uvicorn pydantic requests groq streamlit
```

### Step 2: Start Sentiment API (Terminal 1)
```bash
cd C:\Users\...\Deployment
..\.\venv\Scripts\activate
python app.py
```

**Wait for:** `INFO: Uvicorn running on http://0.0.0.0:8000`

### Step 3: Start AI Agent Chat (Terminal 2)
```bash
cd "C:\Users\...\Agent Implementation"
..\.\venv\Scripts\activate
streamlit run chat_ui.py
```

**Opens at:** http://localhost:8501

### Step 4: Test the System
In the Streamlit UI:
1. Click **"😡 Angry Customer"** sample button
2. See sentiment analysis + LLM response
3. Check decision details (sentiment, confidence, action)

**✅ Done! All 3 components working together.**

---

## ✅ Quick Verification

After setup, verify everything is working:

```bash
# 1. Virtual environment active?
where python
# Should show: ...\Sprout\.venv\Scripts\python.exe

# 2. Model file exists?
dir "Sentiment model\results\model.joblib"
# Should show: model.joblib (file size ~few MB)

# 3. API responds?
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# 4. Streamlit UI accessible?
# Browser should show chat interface at http://localhost:8501

# 5. Test agent CLI (optional)
cd "Agent Implementation"
python agent.py
# Should show 4 test cases with outputs
```

**Troubleshooting:** If any verification fails, see [Troubleshooting](#troubleshooting) section below.

**For detailed usage instructions, see:**
- Agent UI guide: [`Agent Implementation/README.md`](Agent%20Implementation/README.md)
- API documentation: http://localhost:8000/docs
- Complete commands: [`COMMANDS_REFERENCE.md`](COMMANDS_REFERENCE.md)

---

## Project File Structure 

```
Sprout/
├── Sentiment model/          # 1ML Training Pipeline
│   ├── src/                  # Training scripts
│   ├── results/              # Model + predictions
│   └── README.md            # → ML documentation
│
├── Deployment/               # REST API Service
│   ├── app.py               # FastAPI application
│   ├── Dockerfile           # Container config
│   └── README.md            # → API documentation
│
├── Agent Implementation/     # AI Agent + Chat UI
│   ├── agent.py             # Agent logic
│   ├── chat_ui.py           # Streamlit interface
│   └── README.md            # → Agent documentation
│
├── COMMANDS_REFERENCE.md     # All commands
└── sentiment_test_cases_2025.csv
```

---

## Commands Reference

### Usage
```bash
# Terminal 1 - Start API
cd Deployment
..\.venv\Scripts\activate
python app.py

# Terminal 2 - Start Chat UI
cd "Agent Implementation"
..\.venv\Scripts\activate
streamlit run chat_ui.py
```

### Testing
```bash
# Test API
curl http://localhost:8000/health

# Test Agent
cd "Agent Implementation"
python agent.py
```

**For complete command list, see:** [`COMMANDS_REFERENCE.md`](COMMANDS_REFERENCE.md)

---

## Testing

**In Streamlit UI (http://localhost:8501):**
1. Click **"😡 Angry Customer"** → Escalation
2. Click **"🤔 Unclear Message"** → Clarification  
3. Click **"😊 Happy Customer"** → Acknowledgment
4. Click **"😐 Neutral Request"** → Helpful response

**Or test specific components:**
- API: http://localhost:8000/docs (Swagger UI)
- Agent CLI: `python agent.py`
- Simple test: `python test_simple.py`

---

## 🐛 Troubleshooting

### Model File Not Found
```bash
# Check if model exists
dir "Sentiment model\results\model.joblib"

# If missing, train the model
cd "Sentiment model"
python src/run_sentiment.py --input ../sentiment_test_cases_2025.csv --output-dir results
```

### API Connection Refused
```bash
# Check if API is running
curl http://localhost:8000/health

# If not running, start it
cd Deployment
..\.venv\Scripts\activate
python app.py
```

### Port Already in Use
```powershell
# Find process using port 8000 or 8501
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# Kill the process
taskkill /PID <PID> /F
```

### Virtual Environment Issues
```bash
# Deactivate and recreate
deactivate
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate
pip install sentence-transformers scikit-learn pandas numpy joblib fastapi uvicorn pydantic requests groq streamlit
```

### Package Installation Timeout
```bash
# Install with extended timeout
pip install --timeout 300 --retries 10 streamlit groq requests pydantic

# Or install core packages first
pip install requests pydantic groq
python "Agent Implementation/agent.py"  # Test without UI
pip install streamlit  # Install UI later
```

**For more troubleshooting, see:** [`COMMANDS_REFERENCE.md`](COMMANDS_REFERENCE.md)

---

## Key Results

| Component | Metric | Value |
|-----------|--------|-------|
| **ML Model** | Accuracy | 87% |
| **ML Model** | Training Time | ~4s |
| **API** | Response Time | <100ms |
| **API** | Endpoints | 5 |
| **Agent** | End-to-End | <1.5s |
| **Agent** | Actions | 4 types |

**Technology Stack:** Python 3.10+, scikit-learn, FastAPI, Groq (Llama 3.3 70B), Streamlit, Docker

---

## Documentation

- **[`Sentiment model/README.md`](Sentiment%20model/README.md)** - ML training, grid search, hyperparameters
- **[`Deployment/README.md`](Deployment/README.md)** - API endpoints, Docker, testing
- **[`Agent Implementation/README.md`](Agent%20Implementation/README.md)** - Agent setup, decision logic, UI guide
- **[`COMMANDS_REFERENCE.md`](COMMANDS_REFERENCE.md)** - All commands for setup, testing, troubleshooting

---

## Requirements Completed

- ✅ **Task 1:** Sentiment classifier (87% accuracy, embeddings + SVM)
- ✅ **Task 2:** REST API (FastAPI, 5 endpoints, Docker)
- ✅ **Task 3:** AI Agent (Groq LLM, 4 actions, Streamlit UI)

**Status:** Production-ready system with complete documentation

---

## Recommendations for Production Enhancement

This implementation uses classical ML models and local deployment to demonstrate core capabilities within limited computational resources and development time. For production deployment, consider:

### Model & Scoring Improvements
- **Advanced Models**: Transition from classical SVM to transformer-based models (BERT, RoBERTa, DistilBERT) for improved accuracy and nuanced sentiment understanding
- **Better Feature Engineering**: Explore contextualized embeddings (BERT embeddings) instead of sentence-transformers, or fine-tune models on domain-specific data
- **Multi-Label Classification**: Extend beyond 3 classes to capture sentiment intensity (very negative, negative, neutral, positive, very positive)
- **Ensemble Methods**: Combine multiple models (transformer + classical) for improved robustness

### Scoring & Confidence Metrics
- **Beyond TF-IDF**: Current implementation uses sentence embeddings, but could benefit from:
  - Fine-tuned BERT/RoBERTa embeddings
  - Word2Vec or GloVe with attention mechanisms
  - Custom domain-specific embeddings
- **Calibrated Confidence Scores**: Implement probability calibration (Platt scaling, isotonic regression) for more reliable confidence estimates
- **Uncertainty Quantification**: Add Bayesian approaches or ensemble uncertainty for better decision making

### Infrastructure & Deployment
- **Dedicated VM/Cloud Deployment**: Deploy on AWS EC2, GCP Compute Engine, or Azure VMs instead of localhost
- **Container Orchestration**: Use Kubernetes for scalability and load balancing
- **Model Serving**: Implement TensorFlow Serving, TorchServe, or Triton for optimized inference
- **Auto-Scaling**: Configure horizontal pod autoscaling based on traffic patterns
- **CDN & Edge Computing**: Deploy model endpoints at edge locations for reduced latency

### Monitoring & Maintenance
- **Model Monitoring**: Track model drift, data drift, and prediction quality over time
- **A/B Testing Framework**: Compare model versions and decision strategies
- **Logging & Analytics**: Implement comprehensive logging (ELK stack) and analytics dashboards
- **Feedback Loop**: Collect user feedback to continuously retrain and improve the model
- **Performance Metrics**: Monitor API latency, throughput, error rates with Prometheus/Grafana

### Security & Compliance
- **API Authentication**: Implement OAuth2, JWT tokens, or API keys for secure access
- **Rate Limiting**: Protect against abuse with request throttling
- **Data Privacy**: Ensure GDPR/CCPA compliance, implement PII detection and anonymization
- **Secrets Management**: Use HashiCorp Vault or AWS Secrets Manager instead of hardcoded keys

### LLM & Agent Enhancements
- **Model Upgrades**: Experiment with GPT-4, Claude, or other state-of-the-art LLMs
- **Fine-Tuning**: Fine-tune LLMs on company-specific customer support conversations
- **Multi-Agent Systems**: Implement specialized agents for different support categories
- **RAG Integration**: Add retrieval-augmented generation for knowledge-base queries

### Cost Optimization
- **Batch Processing**: Implement batching for high-throughput scenarios
- **Model Quantization**: Use INT8 or FP16 quantization for faster inference
- **Caching**: Cache frequent predictions to reduce API calls
- **Spot Instances**: Use spot/preemptible instances for non-critical workloads

**Note:** Classical models (SVM with sentence embeddings) were chosen for this skill demonstration to balance accuracy, speed, and resource constraints. Production systems should evaluate trade-offs between model complexity, latency requirements, and available infrastructure.

---

**Built for Sprout Solutions Skill Demonstration | December 2025 | [Ethan Serapio](https://www.linkedin.com/in/ethan-serapio-32b2b0220/)**
