# Web-Based Machine Learning System for Cardiovascular Risk Prediction and Analysis

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E.svg)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Academic Alignment:** University of Koblenz — M.Sc. Web and Data Science  
> **Thesis / Project Type:** Scientific Research + Data Science + Web/Data-Intensive Software Engineering  
> **Author:** Mohammad Hasan Talebi ([@tmohammadhasan212](https://github.com/tmohammadhasan212))

---

## 1. Project Overview & Research Motivation

Cardiovascular diseases (CVDs) remain the leading cause of mortality worldwide. Early detection of clinical risk factors provides opportunities for preventive care. However, deploying machine learning in healthcare domains presents twin challenges: **predictive reliability** and **model explainability**.

This project establishes a reproducible, scientifically rigorous data-intensive web system that investigates:
1. **Primary Research Question:** *How do different machine-learning approaches perform for cardiovascular risk prediction, and which patient features contribute most to the resulting predictions?*
2. **Secondary Research Questions:**
   - How do linear baseline, distance-based, decision tree, and ensemble architectures compare across clinical evaluation metrics (Recall, Precision, F1, ROC-AUC)?
   - Can feature engineering based on physiological cardiovascular ratios improve discriminative power without data leakage?
   - How can local and global Explainable AI (XAI) using SHAP (SHapley Additive exPlanations) be integrated into a responsive web application to make individual risk predictions transparent to users?

> **⚠️ Medical Disclaimer:** This system is an academic machine-learning research prototype. It does not provide medical diagnoses, treatment decisions, or clinical recommendations.

---

## 2. Key Features

- **Leakage-Free Preprocessing**: Scikit-learn `ColumnTransformer` with median imputation for continuous features, mode imputation for categorical attributes, and standard scaling learned strictly from training data.
- **7-Model Systematic Comparison**:
  1. *Logistic Regression* (Linear Baseline)
  2. *K-Nearest Neighbors (KNN)* (Instance/Distance-based)
  3. *Decision Tree* (Non-linear rule-based)
  4. *Random Forest* (Bagging Ensemble)
  5. *Support Vector Machine (SVM)* (Kernel-based)
  6. *AdaBoost* (Sequential Adaptive Boosting)
  7. *Gradient Boosting* (Gradient Boosting Decision Trees)
- **Rigorous Evaluation**: Stratified 5-Fold Cross-Validation, Hyperparameter Grid Optimization, and single hold-out evaluation on an untouched test set reporting Accuracy, Precision, Recall/Sensitivity, Specificity, F1-Score, and ROC-AUC.
- **Explainable AI (SHAP)**:
  - *Global Feature Importance*: Summary of clinical determinants across the cohort.
  - *Local Patient Attribution*: Real-time waterfall contribution showing how specific clinical biomarkers push individual risk higher or lower relative to the baseline.
- **Data-Intensive Web Backend**:
  - FastAPI REST API with Pydantic v2 validation.
  - SQLAlchemy ORM with dual-database support: zero-configuration **SQLite** for instant local development and **PostgreSQL** for containerized deployments.
  - Prediction history tracking, filtering, deletion, and CSV export.
- **Interactive Web Interface**: Clean single-page application with clinical form presets, dynamic risk gauge, SHAP attribution visualizations, prediction history, and scientific analytics dashboard.

---

## 3. System Architecture

```text
                    ┌───────────────────────────────────────────┐
                    │          Web Client / Dashboard           │
                    │  (Patient Form, Risk Gauge, XAI, History) │
                    └─────────────────────┬─────────────────────┘
                                          │ HTTP / REST JSON
                                          ▼
                    ┌───────────────────────────────────────────┐
                    │               FastAPI API                 │
                    │    Validation (Pydantic v2) & Routers     │
                    │   /predict  •  /history  •  /model-info   │
                    └──────────┬──────────────────┬─────────────┘
                               │                  │
                ┌──────────────┴──────────┐       │
                ▼                         ▼       ▼
       ┌──────────────────┐    ┌─────────────────────┐
       │   ML Pipeline    │    │  Database (SQL)     │
       │  Preprocessor +  │    │  PredictionRecord   │
       │  Trained Model   │    │  ModelVersion       │
       └────────┬─────────┘    │  (SQLite/Postgres)  │
                │              └─────────────────────┘
                ▼
       ┌──────────────────┐
       │  Explainable AI  │
       │  (SHAP Engine)   │
       └──────────────────┘
```

---

## 4. Repository Structure

```text
cardiovascular-risk-ml-system/
├── data/
│   ├── raw/
│   │   └── heart_disease.csv       # Benchmark UCI Cleveland dataset (303 records)
│   ├── processed/                  # Processed cache
│   └── README.md                   # Data dictionary, clinical ranges, and license
├── src/
│   ├── config.py                   # Central settings, schema & hyperparameter config
│   ├── data/
│   │   ├── loading.py              # Ingestion, validation, stratified train/test split
│   │   └── preprocessing.py        # ColumnTransformer pipeline
│   ├── features/
│   │   └── engineering.py          # Clinical derived feature engineering transformer
│   └── models/
│       ├── train.py                # Automated 7-model training & grid tuning CLI
│       ├── evaluate.py             # Multi-metric evaluation and curve calculation
│       ├── predict.py              # Inference service
│       └── interpret.py            # Global and local SHAP explainability service
├── app/
│   ├── main.py                     # FastAPI application factory & lifespan
│   ├── api/
│   │   ├── routes_prediction.py    # Prediction & batch endpoints
│   │   ├── routes_history.py       # Persistence, filtering, and CSV export
│   │   └── routes_analytics.py     # Evaluation metrics and model metadata
│   ├── schemas/
│   │   └── prediction.py           # Pydantic v2 request/response schemas
│   ├── database/
│   │   ├── connection.py           # SQLAlchemy engine & session factory
│   │   ├── models.py               # ORM tables: PredictionRecord, ModelVersion
│   │   └── repository.py           # Database CRUD abstraction
│   ├── services/
│   │   ├── prediction_service.py   # High-level prediction orchestrator
│   │   └── explanation_service.py  # Local SHAP breakdown wrapper
│   ├── templates/
│   │   └── index.html              # Multi-tab modern web dashboard
│   └── static/
│       ├── css/styles.css          # Health-tech clean UI styling
│       └── js/app.js               # Reactive asynchronous client logic
├── models/
│   ├── best_model.joblib           # Serialized production pipeline
│   └── model_metadata.json         # Evaluation metrics & training metadata
├── tests/
│   ├── test_preprocessing.py       # Pipeline & leakage prevention tests
│   ├── test_models.py              # Training, inference, and SHAP tests
│   ├── test_api.py                 # FastAPI endpoint tests
│   ├── test_database.py            # Database CRUD and persistence tests
│   └── test_integration.py         # Full end-to-end user journey test
├── docs/
│   ├── architecture.md             # System design, data flow, ER diagram
│   ├── methodology.md              # Research question, experiment design, metrics
│   └── api.md                      # OpenAPI specification and sample payloads
├── notebooks/                      # Exploratory data analysis & experiments
├── Dockerfile                      # Production container image
├── docker-compose.yml              # Container orchestration (API + PostgreSQL)
├── pyproject.toml                  # Build metadata & dependency definitions
├── requirements.txt                # Pinned production dependencies
└── README.md                       # Main documentation
```

---

## 5. Quick Start & Installation

### Prerequisites
- Python 3.11 or 3.12
- Git
- (Optional) Docker & Docker Compose

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/tmohammadhasan212/cardiovascular-risk-ml-system.git
cd cardiovascular-risk-ml-system

# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Train the Machine Learning Pipeline

Train all 7 model families, run 5-fold cross-validation, optimize hyperparameters, and serialize the best pipeline:

```bash
python -m src.models.train
```

### 3. Run the Automated Test Suite

```bash
pytest -v --cov=src --cov=app tests/
```

### 4. Launch the Web Application

```bash
uvicorn app.main:app --reload --port 8000
```

Open your browser at:
- **Web Dashboard**: [http://localhost:8000](http://localhost:8000)
- **Interactive API Documentation (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative API Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 6. Running with Docker Compose

To run the application with PostgreSQL:

```bash
docker compose up --build
```

Access the service at [http://localhost:8000](http://localhost:8000).

---

## 7. License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
