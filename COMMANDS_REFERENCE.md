# Complete Commands Reference - Sprout AI Project
## Setup Options

You have **two ways** to set up the project environment:

### Option 1: Download Pre-configured Virtual Environment (Faster)
If available on GitHub, download the `.venv` or `venv` folder to skip the lengthy package installation process. Simply:
1. Download the virtual environment folder from the repository
2. Extract it to the project root directory
3. Activate it and start using the project immediately

**Note:** This works best if you have the same OS and Python version as the environment was created with.

### Option 2: Manual Setup (Recommended for Different OS/Python Version)
Follow the commands below to create your own virtual environment and install all dependencies from scratch. This ensures compatibility with your system.

---
## Quick Start Commands

### Setup (One-Time)
```bash
cd C:\Users\...
python -m venv .venv
.venv\Scripts\activate
pip install sentence-transformers scikit-learn pandas numpy joblib fastapi uvicorn pydantic requests groq streamlit
```

### Daily Usage (2 Terminals)

**Terminal 1 - Sentiment API:**
```bash
cd C:\Users\...\Deployment
..\.venv\Scripts\activate
python app.py
```

**Terminal 2 - AI Agent Chat:**
```bash
cd "C:\Users\...\Agent Implementation"
..\.venv\Scripts\activate
streamlit run chat_ui.py
```

**Access:**
- Chat UI: http://localhost:8501
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## Installation Commands

### Install by Component

**ML Model Dependencies:**
```bash
cd "C:\Users\...\Sentiment model"
pip install sentence-transformers scikit-learn pandas numpy joblib
```

**API Dependencies:**
```bash
cd C:\Users\...\Deployment
pip install fastapi uvicorn pydantic python-multipart
```

**Agent Dependencies:**
```bash
cd "C:\Users\...\Agent Implementation"
pip install requests pydantic groq streamlit
```

### Install Everything at Once
```bash
cd C:\Users\...
.venv\Scripts\activate
pip install sentence-transformers scikit-learn pandas numpy joblib fastapi uvicorn pydantic python-multipart requests groq streamlit
```

### If Installation Fails (Slow Internet)
```bash
# Install minimal packages first
pip install --timeout 300 --retries 10 requests pydantic groq

# Test agent without UI
python agent.py

# Install Streamlit later
pip install --timeout 600 --retries 20 streamlit
```

---

## Testing Commands

### Test Sentiment API

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Single Prediction:**
```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"text\":\"This is terrible!\"}"
```

**Batch Prediction:**
```bash
curl -X POST http://localhost:8000/batch_predict -H "Content-Type: application/json" -d "{\"texts\":[\"I love it!\",\"This is bad\",\"It's okay\"]}"
```

**Model Info:**
```bash
curl http://localhost:8000/model/info
```

**In Browser:**
- Interactive API: http://localhost:8000/docs
- API Reference: http://localhost:8000/redoc

### Test Agent

**Command-Line Test (4 sample cases):**
```bash
cd "C:\Users\...\Agent Implementation"
python agent.py
```

**Simple Quick Test:**
```bash
python test_simple.py
```

**With Chat UI:**
```bash
streamlit run chat_ui.py
```
Then click sample buttons or type messages.

---

## Model Training Commands

### Train Sentiment Model
```bash
cd "C:\Users\...\Sentiment model"
..\.venv\Scripts\activate
python src/run_sentiment.py --input ../sentiment_test_cases_2025.csv --output-dir results
```

**Output:**
- `results/model.joblib` - Trained model
- `results/output_sentiment_test.csv` - Predictions
- `results/metrics.txt` - Performance metrics

### Run Grid Search Optimization
```bash
cd "C:\Users\...\Sentiment model"
python src/grid_search_adv.py --input ../sentiment_test_cases_2025.csv --output-dir results
```

**Runtime:** ~5-10 minutes (180 combinations)

**Output:**
- `results/best_hyperparams.json` - Best parameters
- Console output with top 10 configurations

---

## Docker Commands (Optional)

### Build and Run API Container

**Using Docker:**
```bash
cd C:\Users\...\Deployment

# Build image
docker build -t sentiment-api .

# Run container
docker run -p 8000:8000 sentiment-api

# Run in background
docker run -d -p 8000:8000 sentiment-api

# Stop container
docker ps
docker stop <container_id>
```

**Using Docker Compose:**
```bash
cd C:\Users\...\Deployment

# Start
docker-compose up

# Start in background
docker-compose up -d

# Stop
docker-compose down

# Rebuild and start
docker-compose up --build
```

---

## Troubleshooting Commands

### Check Service Status

**Check if ports are in use:**
```powershell
# Port 8000 (API)
netstat -ano | findstr :8000

# Port 8501 (Streamlit)
netstat -ano | findstr :8501
```

**Kill process on port:**
```powershell
# Find PID
netstat -ano | findstr :8000

# Kill it
taskkill /PID <PID> /F
```

### Verify Environment

**Check Python version:**
```bash
python --version
# Should be: Python 3.10 or higher
```

**Check virtual environment:**
```bash
where python
# Should show: C:\Users\...\.venv\Scripts\python.exe
```

**List installed packages:**
```bash
pip list
```

**Check specific packages:**
```bash
pip list | findstr "streamlit groq fastapi scikit-learn sentence-transformers"
```

### Fix Installation Issues

**Clear pip cache:**
```bash
pip cache purge
```

**Reinstall package:**
```bash
pip uninstall streamlit
pip install --no-cache-dir streamlit
```

**Install with verbose output:**
```bash
pip install -v streamlit
```

**Update pip:**
```bash
python -m pip install --upgrade pip
```

---

## Restart Services

### Restart API
```bash
# In API terminal, press Ctrl+C
cd C:\Users\...\Deployment
python app.py
```

### Restart Streamlit
```bash
# In Streamlit terminal, press Ctrl+C
cd "C:\Users\...\Agent Implementation"
streamlit run chat_ui.py
```

### Force Restart (if hung)
```powershell
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Then restart normally
```

---

## File Navigation Commands

### List Project Structure
```bash
cd C:\Users\...
dir

cd "Sentiment model"
dir

cd ..\Deployment
dir

cd "..\Agent Implementation"
dir
```

### View File Contents
```bash
# View model results
type "Sentiment model\results\metrics.txt"

# View best hyperparameters
type "Sentiment model\results\best_hyperparams.json"

# View requirements
type "Agent Implementation\requirements.txt"
```

### Check Output Files
```bash
# Check if model exists
dir "Sentiment model\results\model.joblib"

# Check predictions
type "Sentiment model\results\output_sentiment_test.csv" | more

# Count lines in dataset
type sentiment_test_cases_2025.csv | find /c /v ""
```

---

## 🧹 Cleanup Commands

### Remove Python Cache
```bash
cd C:\Users\...
rmdir /s /q __pycache__
rmdir /s /q "Sentiment model\__pycache__"
rmdir /s /q "Deployment\__pycache__"
rmdir /s /q "Agent Implementation\__pycache__"
```

### Clear Streamlit Cache
```bash
streamlit cache clear
```

### Remove Virtual Environment (to recreate)
```bash
cd C:\Users\...
deactivate
rmdir /s /q .venv
```

### Recreate Environment
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r "Sentiment model\requirements.txt"
pip install -r Deployment\requirements.txt
pip install -r "Agent Implementation\requirements.txt"
```

---

## Common Workflows

### First Time Setup
```bash
# 1. Create environment
cd C:\Users\...
python -m venv .venv
.venv\Scripts\activate

# 2. Install all dependencies
pip install sentence-transformers scikit-learn pandas numpy joblib fastapi uvicorn pydantic requests groq streamlit

# 3. Train model (if not already trained)
cd "Sentiment model"
python src/run_sentiment.py --input ../sentiment_test_cases_2025.csv --output-dir results

# 4. Done! Now use daily workflow
```

### Daily Development
```bash
# Terminal 1 - API
cd C:\Users\...\Deployment
..\.venv\Scripts\activate
python app.py

# Terminal 2 - Agent UI
cd "C:\Users\...\Agent Implementation"
..\.venv\Scripts\activate
streamlit run chat_ui.py
```

### Testing Everything
```bash
# 1. Test API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"text\":\"This is great!\"}"

# 2. Test Agent CLI
cd "C:\Users\...\Agent Implementation"
python agent.py

# 3. Test Agent UI
# Click sample buttons in http://localhost:8501
```

### Updating Agent Code
```bash
# 1. Stop Streamlit (Ctrl+C)

# 2. Edit files
notepad agent.py
# OR
notepad chat_ui.py

# 3. Restart Streamlit
streamlit run chat_ui.py
```

---

## Environment Variables (Optional)

### Set Groq API Key
```powershell
# PowerShell
$env:GROQ_API_KEY="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"

# CMD
set GROQ_API_KEY=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

# Linux/Mac
export GROQ_API_KEY="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"
```

### Set Sentiment API URL
```powershell
# PowerShell
$env:SENTIMENT_API_URL="http://localhost:8000"

# CMD
set SENTIMENT_API_URL=http://localhost:8000

# Linux/Mac
export SENTIMENT_API_URL="http://localhost:8000"
```

### Check Environment Variables
```powershell
# PowerShell
$env:GROQ_API_KEY
$env:SENTIMENT_API_URL

# CMD
echo %GROQ_API_KEY%
echo %SENTIMENT_API_URL%

# Linux/Mac
echo $GROQ_API_KEY
echo $SENTIMENT_API_URL
```

---

## Performance Monitoring

### Check API Response Time
```bash
# Windows
curl -w "@curl-format.txt" -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"text\":\"Test\"}"

# Simple timing
powershell "Measure-Command {curl http://localhost:8000/health}"
```

### Monitor Logs
```bash
# API logs are shown in Terminal 1
# Streamlit logs are shown in Terminal 2
# Watch for errors or warnings
```

---

## Learning Commands

### Explore API Interactively
```bash
# Open in browser
start http://localhost:8000/docs

# Try different endpoints
# Use "Try it out" button
```

### Explore Model Outputs
```bash
# View predictions
type "Sentiment model\results\output_sentiment_test.csv" | more

# View metrics
type "Sentiment model\results\metrics.txt"

# View hyperparameters
type "Sentiment model\results\best_hyperparams.json"
```

### Read Documentation
```bash
# View README files
type README.md | more
type "Sentiment model\README.md" | more
type "Deployment\README.md" | more
type "Agent Implementation\README.md" | more
```

---

## Verification Checklist

After setup, verify everything works:

```bash
# 1. Virtual environment active?
where python
# Should show: .venv\Scripts\python.exe

# 2. All packages installed?
pip list | findstr "streamlit groq fastapi scikit-learn sentence-transformers"

# 3. Model exists?
dir "Sentiment model\results\model.joblib"

# 4. API running?
curl http://localhost:8000/health

# 5. Streamlit running?
# Visit http://localhost:8501

# 6. Agent working?
cd "Agent Implementation"
python agent.py

```

---

**Last Updated:** December 27, 2025  
**Project:** Sprout AI Technical Task  
**Status:** Complete and Functional
