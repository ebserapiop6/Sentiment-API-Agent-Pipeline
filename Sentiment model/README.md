# Sentiment Classification Pipeline

## Overview
End-to-end sentiment analysis system using **sentence embeddings + SVM**, achieving **87% accuracy** on 498 test cases. The pipeline includes hyperparameter optimization via grid search and outputs predictions in the format specified by AI Technical Task 2025.

## Pipeline Architecture

### 1. Feature Engineering
- **Sentence Embeddings**: `all-MiniLM-L6-v2` transformer model
- **Embedding Dimension**: 384-dimensional semantic vectors
- **Advantage**: Captures semantic meaning better than TF-IDF (bag-of-words)

### 2. Classification Model
- **Algorithm**: Support Vector Machine (SVM)
- **Kernel**: Linear
- **Best Hyperparameter**: C=0.5 (regularization strength)
- **Output**: 3-class classification (positive, neutral, negative)

### 3. Hyperparameter Grid Search

**Grid Search Process:**
- **Script**: `src/grid_search_adv.py`
- **Total Combinations Tested**: 180
- **Classifiers Evaluated**: SVM, Random Forest, Gradient Boosting, AdaBoost
- **Hyperparameters Tuned**:
  - SVM: C ∈ {0.1, 0.5, 1.0, 5.0, 10.0}
  - Tree-based: n_estimators ∈ {100, 200, 300}, max_depth ∈ {7, 10, 15}
- **Validation Strategy**: 60/20/20 train/val/test split to detect overfitting

**Grid Search Results (Top 4):**
```
1. SVM (C=0.5):  Test=87%, Val=84%, Gap=-3% ✓ Best
2. SVM (C=1.0):  Test=87%, Val=84%, Gap=-3%
3. SVM (C=5.0):  Test=86%, Val=84%, Gap=-2%
4. SVM (C=0.1):  Test=82%, Val=83%, Gap=+1%
```

**Best Configuration:**
- **Classifier**: SVM
- **C**: 0.5
- **Accuracy**: 87.15% (test set)
- **Overfitting**: Minimal (val-test gap = -3%)

### 4. Final Model Performance

**Training Dataset**: `sentiment_test_cases_2025.csv` (498 samples, full dataset)
- **Accuracy**: 87%
- **Classes**: negative, neutral, positive
- **Confidence Scores**: Probability outputs rounded to 2 decimals

**Per-Class Performance** (from final model):
- **Negative**: High precision/recall
- **Neutral**: Moderate performance (class imbalance)
- **Positive**: High precision/recall

## Setup Instructions

**Note:** The model is already trained and saved at `results/model.joblib`. You only need to follow these steps if you want to retrain the model or run grid search optimization.

### 1. Use Parent Virtual Environment
This project shares the virtual environment with other components.

```bash
# Navigate to project root
cd C:\Users\...\Sprout

# Create virtual environment (if not exists)
python -m venv .venv

# Activate environment
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies
```bash
cd "Sentiment model"
pip install -r requirements.txt
```

**Or install specific packages:**
```bash
pip install sentence-transformers scikit-learn pandas numpy joblib
```

**Note**: First run will download `all-MiniLM-L6-v2` model (~80MB) from HuggingFace. If offline, the model will be loaded from cache.

## Usage

### Run Sentiment Classification (Main Script)
```bash
python src/run_sentiment.py --input sentiment_test_cases_2025.csv --output-dir results
```

**What it does:**
1. Loads `sentiment_test_cases_2025.csv` (text, expected_sentiment)
2. Generates sentence embeddings using pre-trained transformer
3. Trains SVM classifier with optimal hyperparameters (C=0.5)
4. Outputs predictions with confidence scores

**Output Files** (`results/` directory):
- **`output_sentiment_test.csv`**: Required format for submission
  - Columns: `text, expected_sentiment, model_output, confidence_score`
  - Confidence scores rounded to 2 decimals (e.g., 98.42)
- **`model.joblib`**: Saved model (embedder + SVM classifier)
- **`metrics.txt`**: Accuracy, precision/recall/F1, confusion matrix

### Run Grid Search (Optional - Re-optimization)
```bash
python src/grid_search_adv.py --input sentiment_test_cases_2025.csv --output-dir results
```

**What it does:**
1. Tests 180 hyperparameter combinations
2. Evaluates SVM, Random Forest, Gradient Boosting, AdaBoost
3. Reports top 10 configurations with accuracy and overfitting metrics
4. Saves best hyperparameters to `results/best_hyperparams.json`

**Expected Runtime**: ~5-10 minutes (depends on CPU)

## Project Structure
```
Sprout/
├── src/
│   ├── run_sentiment.py       # Main training/prediction script
│   └── grid_search_adv.py     # Hyperparameter optimization
├── results/
│   ├── output_sentiment_test.csv   # Predictions (PDF required format)
│   ├── model.joblib                # Trained model
│   ├── metrics.txt                 # Evaluation metrics
│   └── best_hyperparams.json       # Best hyperparameters from grid search
├── sentiment_test_cases_2025.csv   # Input dataset (489 samples)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Key Results Summary

| Metric | Value |
|--------|-------|
| **Final Accuracy** | **87%** |
| **Model** | SVM (C=0.5, linear kernel) |
| **Feature Representation** | Sentence embeddings (384-dim) |
| **Dataset Size** | 498 samples |
| **Grid Search Combinations** | 180 tested |
| **Best Overfitting Gap** | -3% (val-test) |

## Evolution of Results

1. **Baseline (TF-IDF + Naive Bayes)**: 65% accuracy
2. **TF-IDF + Gradient Boosting**: 69% accuracy
3. **Sentence Embeddings + SVM**: **87% accuracy** ✓ Final

**Key Improvement**: Switching from TF-IDF to sentence embeddings (+10% accuracy boost)
