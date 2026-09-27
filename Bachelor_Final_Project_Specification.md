# Web-Based Machine Learning System for Cardiovascular Risk Prediction and Analysis

## Project Specification & Implementation Requirements

**Target:** Bachelor's final-year project / scientific thesis  
**Project Scope:** Final Bachelor's Graduation Project in Computer Science / Software Engineering  
**Suggested project type:** Scientific research + data science + web/data-intensive software system  
**Recommended language:** English  
**Core stack:** Python, pandas, NumPy, scikit-learn, FastAPI, SQL database, HTML/CSS/JavaScript or a lightweight frontend, Docker

---

## 1. Executive Summary

This project develops and scientifically evaluates a web-based, data-intensive machine-learning system for cardiovascular risk prediction.

The project has two equally important dimensions:

1. **Scientific/Data Science:** investigate how different machine-learning methods perform on a cardiovascular-risk prediction task, including preprocessing, feature engineering, model selection, evaluation, and model interpretability.
2. **Web/Data-Intensive Engineering:** turn the resulting workflow into a usable web system with a backend API, persistent database, prediction service, data visualization, and reproducible software architecture.

The project must not be presented merely as "a website that runs a machine-learning model." The central academic contribution is a reproducible investigation of a defined research question, supported by systematic experiments and a properly documented software system.

### Suggested thesis title

> **Design and Development of a Web-Based Machine Learning System for Cardiovascular Risk Prediction and Analysis**

Alternative, more research-oriented title:

> **A Comparative Study of Machine Learning Methods for Cardiovascular Risk Prediction with a Web-Based Data-Intensive Implementation**

---

# 2. Motivation

Cardiovascular diseases are an important application domain for predictive data analysis. Machine-learning methods can identify relationships between patient characteristics and cardiovascular outcomes, but different algorithms can exhibit different predictive performance and interpretability.

The project therefore investigates:

- how different machine-learning algorithms perform on the selected dataset;
- which features contribute most strongly to predictions;
- how preprocessing and feature engineering affect performance;
- whether the best-performing model provides a meaningful trade-off between predictive performance and interpretability;
- how a trained model can be integrated into a reproducible web-based data system.

The project combines machine learning, data analysis, software engineering, databases, web development, and scientific evaluation.

---

# 3. Main Research Question

## Primary research question

> **How do different machine-learning approaches perform for cardiovascular risk prediction, and which patient features contribute most to the resulting predictions?**

## Secondary research questions

1. Which preprocessing strategy produces the most reliable model performance?
2. How do linear, tree-based, instance-based, and ensemble methods compare?
3. Which evaluation metrics provide the most informative assessment for this classification problem?
4. Which patient features have the greatest influence on model predictions?
5. How can the selected model be integrated into a maintainable web-based data-intensive system?
6. Can the system provide understandable explanations for individual predictions?

---

# 4. Project Objectives

The project must achieve the following objectives.

### O1 — Data acquisition and understanding
Obtain a legally usable cardiovascular dataset and document its origin, attributes, limitations, and licensing/usage conditions.

### O2 — Data analysis
Perform exploratory data analysis (EDA), statistical analysis, missing-value analysis, outlier inspection, class-distribution analysis, and feature investigation.

### O3 — Data preprocessing
Build a reproducible preprocessing pipeline covering:

- missing values;
- categorical encoding;
- numerical scaling where appropriate;
- outlier handling where justified;
- train/validation/test separation;
- prevention of data leakage.

### O4 — Feature engineering
Investigate whether meaningful transformations or derived features improve model performance.

### O5 — Model development
Train and compare several machine-learning algorithms.

### O6 — Model evaluation
Evaluate models using multiple appropriate metrics and statistically/reproducibly compare their results.

### O7 — Explainability
Use model-interpretability techniques to identify important features and explain individual predictions.

### O8 — Web system
Build a web application through which users can:

- enter patient information;
- request a prediction;
- view the prediction;
- view confidence/probability information where appropriate;
- inspect relevant explanatory information;
- review previously submitted cases if persistence is enabled.

### O9 — Backend/API
Expose prediction functionality through a clean API.

### O10 — Database
Store application data using a relational database.

### O11 — Testing
Test data-processing components, API endpoints, prediction behavior, and major application functionality.

### O12 — Reproducibility
Provide a reproducible environment and clear instructions for running the complete system.

---

# 5. Scope

## Included

- supervised binary classification;
- structured/tabular patient data;
- exploratory data analysis;
- preprocessing;
- feature engineering;
- multiple ML algorithms;
- hyperparameter optimization;
- model evaluation;
- model interpretation;
- REST API;
- web interface;
- relational database;
- automated tests;
- documentation;
- scientific thesis/report.

## Not included

The system is **not** a medical diagnostic tool.

It must not claim to diagnose, treat, or medically clear a patient.

Predictions must be presented as outputs of an academic machine-learning experiment and not as medical advice.

---

# 6. Recommended Dataset

A small, well-documented cardiovascular dataset may be used for a bachelor's project.

A commonly used starting point is the UCI Heart Disease dataset or another openly licensed cardiovascular dataset.

Before implementation, document:

- dataset source;
- URL/reference;
- license;
- number of records;
- number of features;
- target definition;
- missing values;
- categorical variables;
- numerical variables;
- known limitations;
- potential bias;
- whether the dataset is suitable for the intended research question.

If the original dataset contains a small number of observations, explicitly discuss the limitations of statistical generalization.

---

# 7. Expected Data Schema

A possible schema based on a common heart-disease dataset is:

| Feature | Type | Description |
|---|---|---|
| age | numerical | Patient age |
| sex | categorical/binary | Patient sex |
| cp | categorical | Chest-pain category |
| trestbps | numerical | Resting blood pressure |
| chol | numerical | Serum cholesterol |
| fbs | binary | Fasting blood sugar indicator |
| restecg | categorical | Resting ECG result |
| thalach | numerical | Maximum heart rate |
| exang | binary | Exercise-induced angina |
| oldpeak | numerical | ST depression |
| slope | categorical | ST-segment slope |
| ca | numerical/categorical | Number of major vessels |
| thal | categorical | Thalassemia-related attribute |
| target | binary | Prediction target |

The exact schema must follow the selected dataset rather than being assumed.

---

# 8. System Architecture

The recommended architecture is:

```text
                    ┌─────────────────────┐
                    │     Web Client      │
                    │  Patient Data Form  │
                    └──────────┬──────────┘
                               │ HTTP/JSON
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    │                     │
                    │ Validation           │
                    │ Prediction endpoint  │
                    │ History endpoint     │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
       ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
       │ ML Pipeline  │ │   Database   │ │  Explainable │
       │ Preprocessor │ │ PostgreSQL/  │ │  Prediction  │
       │ Model        │ │ SQLite       │ │   / SHAP     │
       └──────────────┘ └──────────────┘ └──────────────┘
                │
                ▼
       ┌──────────────────┐
       │ Saved Model /    │
       │ Model Metadata   │
       └──────────────────┘
```

---

# 9. Recommended Technology Stack

## Programming

- Python 3.11+
- type hints
- virtual environment
- PEP 8-compatible formatting

## Data Science

- NumPy
- pandas
- Matplotlib
- scikit-learn
- optionally SciPy
- optionally SHAP

## Backend

Recommended:

- FastAPI
- Pydantic
- Uvicorn

Alternative:

- Flask

FastAPI is preferred because it naturally supports typed request/response models and automatic API documentation.

## Database

Recommended:

- PostgreSQL for the full implementation

For local development:

- SQLite may be used initially.

Recommended ORM:

- SQLAlchemy

## Frontend

A simple frontend is sufficient.

Possible options:

- HTML/CSS/JavaScript
- React

For a bachelor's project, a simple HTML/CSS/JavaScript frontend is acceptable if the backend and scientific component are strong.

## Development tools

- Git
- GitHub
- pytest
- Ruff
- Docker / Docker Compose
- optional pre-commit

---

# 10. Repository Structure

Recommended structure:

```text
cardiovascular-risk-ml-system/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── .gitignore
├── .env.example
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_model_comparison.ipynb
│   └── 05_interpretability.ipynb
│
├── src/
│   ├── data/
│   │   ├── loading.py
│   │   └── preprocessing.py
│   │
│   ├── features/
│   │   └── engineering.py
│   │
│   ├── models/
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   ├── predict.py
│   │   └── interpret.py
│   │
│   └── config.py
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── routes_prediction.py
│   │   └── routes_history.py
│   │
│   ├── schemas/
│   │   └── prediction.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repository.py
│   │
│   ├── services/
│   │   ├── prediction_service.py
│   │   └── explanation_service.py
│   │
│   └── templates/
│       └── index.html
│
├── models/
│   ├── best_model.joblib
│   └── model_metadata.json
│
├── tests/
│   ├── test_preprocessing.py
│   ├── test_models.py
│   ├── test_api.py
│   └── test_database.py
│
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   └── api.md
│
└── thesis/
    └── thesis.pdf
```

---

# 11. Data Science Pipeline

The ML pipeline must be reproducible.

```text
Raw Dataset
     ↓
Data Validation
     ↓
Exploratory Data Analysis
     ↓
Train/Test Split
     ↓
Preprocessing
     ↓
Feature Engineering
     ↓
Cross-Validation
     ↓
Model Training
     ↓
Hyperparameter Optimization
     ↓
Model Evaluation
     ↓
Model Interpretation
     ↓
Model Selection
     ↓
Model Serialization
     ↓
Deployment
```

---

# 12. Data Validation

Before training:

- verify expected columns;
- verify data types;
- identify missing values;
- identify duplicated records;
- inspect impossible values;
- inspect target distribution;
- verify categorical domains;
- document all data-cleaning decisions.

Every cleaning decision must be justified.

Do not silently remove observations.

---

# 13. Exploratory Data Analysis

The EDA should include:

### Univariate analysis

- age distribution;
- blood-pressure distribution;
- cholesterol distribution;
- maximum heart-rate distribution;
- target distribution.

### Bivariate analysis

Investigate relationships between selected features and the target.

Examples:

- age vs target;
- sex vs target;
- chest-pain type vs target;
- maximum heart rate vs target;
- exercise-induced angina vs target.

### Correlation analysis

Use appropriate correlation measures for numerical variables.

Do not interpret correlation as causation.

### Class balance

Report:

```text
Number of class 0 samples
Number of class 1 samples
Class percentages
```

If imbalance exists, discuss its implications.

---

# 14. Train/Validation/Test Strategy

Avoid evaluating the model on data used to tune it.

Recommended approach:

- hold out a final test set;
- use stratified cross-validation on the training set;
- perform hyperparameter optimization only within the training process;
- evaluate the final selected model once on the untouched test set.

Example:

```text
Complete Dataset
       │
       ├── 80% Training
       │      └── Stratified 5-fold CV
       │             └── Hyperparameter tuning
       │
       └── 20% Final Test
              └── Final evaluation
```

Use a fixed random seed for reproducibility where appropriate.

---

# 15. Preprocessing Requirements

Use scikit-learn pipelines and transformers whenever possible.

Possible steps:

### Numerical features

- imputation if necessary;
- scaling for algorithms that require it.

### Categorical features

- imputation if necessary;
- One-Hot Encoding or another justified encoding.

### Critical requirement

Preprocessing parameters must be learned only from the training data.

Do not fit a scaler or encoder on the entire dataset before splitting.

This prevents data leakage.

---

# 16. Feature Engineering

Feature engineering should be limited to transformations that can be scientifically justified.

Possible experiments:

- age groups;
- clinically meaningful interactions if justified;
- transformed numerical variables;
- grouped categorical variables.

Every engineered feature must be documented.

Do not create dozens of arbitrary features simply to improve a score.

---

# 17. Models to Compare

At least five different model families should be evaluated.

Recommended:

### Baseline

- Logistic Regression

### Tree-based

- Decision Tree
- Random Forest

### Distance/kernel-based

- K-Nearest Neighbors
- Support Vector Machine

### Ensemble

- AdaBoost
- Gradient Boosting
- optionally XGBoost if the environment permits it

A reasonable final comparison could contain:

```text
1. Logistic Regression
2. KNN
3. Decision Tree
4. Random Forest
5. SVM
6. AdaBoost
7. Gradient Boosting
```

Do not add models without a reason.

---

# 18. Hyperparameter Optimization

Use a reproducible optimization strategy.

Recommended:

- GridSearchCV for a small search space;
- RandomizedSearchCV for a larger search space.

Example parameters:

### Random Forest

- n_estimators
- max_depth
- min_samples_split
- min_samples_leaf

### SVM

- C
- kernel
- gamma

### KNN

- n_neighbors
- weights
- metric

### Logistic Regression

- C
- penalty
- solver

The search space must be documented.

---

# 19. Evaluation Metrics

Do not rely only on accuracy.

Report:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

Depending on the final research question, also consider:

- PR-AUC;
- specificity;
- sensitivity.

The choice of primary metric must be justified.

For a health-related classification task, discuss why false negatives and false positives may have different implications.

---

# 20. Statistical Reliability

Because the dataset may be relatively small, avoid presenting a single score as definitive evidence.

Report:

- cross-validation mean;
- cross-validation standard deviation;
- final test performance;
- confidence intervals where feasible;
- limitations caused by sample size.

If statistical significance tests are used, explain why the selected test is appropriate.

---

# 21. Model Selection

Model selection must not be based solely on the highest accuracy.

Consider:

- predictive performance;
- stability across folds;
- calibration where relevant;
- interpretability;
- computational cost;
- deployment complexity.

The final model-selection decision must be explicitly justified in the thesis.

---

# 22. Model Explainability

Implement explainability for the selected model.

Possible tools:

- SHAP;
- permutation importance;
- feature importance for tree models.

The system should provide:

### Global explanation

Which features generally influence model predictions?

### Local explanation

Why did the model produce this particular prediction?

Example output:

```text
Prediction: Higher predicted risk

Important contributing features:
- Feature A
- Feature B
- Feature C

Model probability:
0.78
```

Do not describe feature importance as medical causation.

---

# 23. Model Serialization

The final trained pipeline should be saved as a single deployable artifact where practical.

For example:

```text
models/
    cardiovascular_pipeline.joblib
```

The artifact should contain:

- preprocessing;
- feature transformations;
- trained model.

This minimizes the risk of applying preprocessing differently in production.

Also save metadata:

```json
{
  "model_name": "RandomForest",
  "training_date": "...",
  "dataset_version": "...",
  "features": [],
  "evaluation_metrics": {}
}
```

---

# 24. Backend Requirements

Implement a REST API.

## Health endpoint

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

## Prediction endpoint

```http
POST /api/v1/predict
```

Example request:

```json
{
  "age": 55,
  "sex": 1,
  "cp": 2,
  "trestbps": 140,
  "chol": 250,
  "fbs": 0,
  "restecg": 1,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 1.2,
  "slope": 1,
  "ca": 0,
  "thal": 2
}
```

Example response:

```json
{
  "prediction": 1,
  "probability": 0.78,
  "model_version": "1.0.0"
}
```

The exact response should clearly state that this is a machine-learning prediction, not a medical diagnosis.

---

# 25. Database Requirements

Use a relational database.

Suggested tables:

## prediction_records

```text
id
created_at
input_data
prediction
probability
model_version
```

If JSON storage is undesirable, normalize the input fields into columns.

## model_versions

```text
id
version
model_name
training_date
dataset_version
metrics
```

The database design should be documented with an ER diagram.

---

# 26. Web Interface

The web application should contain at least:

### Page 1 — Prediction form

Fields for all required model inputs.

Requirements:

- validation;
- clear labels;
- sensible input ranges;
- categorical dropdowns where appropriate;
- error messages.

### Page 2 — Prediction result

Display:

- prediction;
- probability/confidence information;
- model version;
- explanation;
- disclaimer.

### Page 3 — Prediction history

Display previous predictions stored in the database.

Optional:

- filtering;
- sorting;
- deletion;
- export.

### Page 4 — Data/Model information

Explain:

- dataset;
- model;
- evaluation;
- limitations.

---

# 27. Data Visualization

Include meaningful visualizations.

Recommended:

- target distribution;
- feature distributions;
- correlation visualization;
- model-performance comparison;
- confusion matrix;
- ROC curves;
- feature importance;
- SHAP summary plot.

Do not add visualizations merely for appearance.

Every important visualization should answer a question.

---

# 28. Software Engineering Requirements

The project must demonstrate proper software engineering.

Requirements:

- modular architecture;
- separation of concerns;
- meaningful naming;
- type hints;
- configuration management;
- environment variables for secrets;
- error handling;
- logging;
- input validation;
- unit tests;
- API tests;
- documentation.

Avoid putting the entire application in one Python file.

---

# 29. Testing

Minimum test categories:

## Unit tests

Test:

- preprocessing;
- feature transformations;
- model loading;
- prediction formatting.

## API tests

Test:

- valid prediction;
- invalid input;
- missing fields;
- incorrect data types;
- health endpoint.

## Database tests

Test:

- creating prediction records;
- retrieving records;
- model metadata.

## Integration test

Test the complete flow:

```text
HTTP request
    ↓
Validation
    ↓
Prediction service
    ↓
Database
    ↓
HTTP response
```

---

# 30. API Documentation

FastAPI's automatically generated OpenAPI documentation should be available.

Expected endpoints should be documented with:

- endpoint description;
- request schema;
- response schema;
- possible errors;
- example requests;
- example responses.

Also create:

```text
docs/api.md
```

---

# 31. Security and Privacy

Even though this is an academic project, security must be considered.

Requirements:

- do not store real patient identities;
- do not collect names;
- do not collect addresses;
- do not collect unnecessary personal information;
- validate all user input;
- never commit secrets;
- use environment variables;
- document the privacy limitations of the dataset.

If synthetic/demo data are used in the deployed system, explicitly state this.

---

# 32. Ethical Requirements

The thesis must include an ethics/limitations section.

Discuss:

- dataset bias;
- demographic representation;
- sample size;
- possible selection bias;
- measurement bias;
- model uncertainty;
- false positives;
- false negatives;
- limitations of historical datasets;
- risks of interpreting correlations as causation;
- limitations of deploying a model trained on a small dataset.

The system must clearly state:

> This system is an academic machine-learning prototype and is not intended for medical diagnosis or clinical decision-making.

---

# 33. Reproducibility

A new user should be able to clone the repository and reproduce the main results.

README must explain:

1. prerequisites;
2. environment setup;
3. dataset acquisition;
4. preprocessing;
5. model training;
6. evaluation;
7. application startup;
8. database startup;
9. tests.

Example:

```bash
git clone <repository>
cd cardiovascular-risk-ml-system

python -m venv .venv
source .venv/bin/activate

pip install -e .

pytest

uvicorn app.main:app --reload
```

If Docker is used:

```bash
docker compose up --build
```

---

# 34. Docker Requirements

Recommended services:

```text
app
database
```

Optional:

```text
frontend
```

The application should run through:

```bash
docker compose up --build
```

The README should document ports and environment variables.

---

# 35. Git Requirements

Use Git throughout development.

Recommended branch structure:

```text
main
develop
feature/data-pipeline
feature/ml-training
feature/api
feature/frontend
feature/testing
```

Commit messages should describe meaningful changes.

Example:

```text
feat: add preprocessing pipeline
feat: implement model comparison
feat: add prediction API
test: add API validation tests
docs: document model evaluation
```

---

# 36. Documentation Requirements

The repository must contain:

### README.md

- project overview;
- motivation;
- architecture;
- setup;
- usage;
- API;
- testing;
- limitations.

### architecture.md

- architecture diagram;
- component descriptions;
- data flow;
- deployment model.

### methodology.md

- dataset;
- preprocessing;
- models;
- evaluation;
- experimental design.

### API documentation

- endpoints;
- schemas;
- examples.

---

# 37. Scientific Experiment Design

The experiment should follow a controlled structure.

## Experiment A — Baseline

Train Logistic Regression with a documented preprocessing pipeline.

## Experiment B — Model comparison

Compare all selected algorithms using identical train/test methodology.

## Experiment C — Hyperparameter optimization

Optimize selected models.

## Experiment D — Feature engineering

Compare baseline features against justified engineered features.

## Experiment E — Explainability

Analyze feature importance and individual predictions.

## Experiment F — Final evaluation

Evaluate the selected model on the untouched test set.

---

# 38. Results Table

The thesis should include a table similar to:

| Model | CV Accuracy | CV F1 | CV ROC-AUC | Test Accuracy | Test F1 | Test ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | | | | | | |
| KNN | | | | | | |
| Decision Tree | | | | | | |
| Random Forest | | | | | | |
| SVM | | | | | | |
| AdaBoost | | | | | | |
| Gradient Boosting | | | | | | |

Do not fabricate or fill results before running the experiments.

---

# 39. Performance Requirements

The project does not need production-scale performance.

Reasonable targets:

- prediction endpoint responds within a few seconds on local hardware;
- model is loaded once at application startup rather than retrained per request;
- database queries for prediction history are responsive;
- training time is documented.

The scientific quality of the experiment is more important than premature optimization.

---

# 40. Definition of Done

The project is considered complete when all of the following are satisfied:

### Data

- [ ] Dataset source documented
- [ ] License/usage conditions documented
- [ ] Dataset validated
- [ ] EDA completed
- [ ] Data limitations discussed

### ML

- [ ] Reproducible preprocessing pipeline
- [ ] At least five model families compared
- [ ] Cross-validation performed
- [ ] Hyperparameter tuning performed
- [ ] Multiple evaluation metrics reported
- [ ] Final test evaluation performed
- [ ] Model interpretation implemented

### Web

- [ ] Backend implemented
- [ ] REST API implemented
- [ ] Prediction endpoint implemented
- [ ] Input validation implemented
- [ ] Web interface implemented
- [ ] Prediction history implemented
- [ ] Model/data information page implemented

### Database

- [ ] Relational database implemented
- [ ] Prediction records stored
- [ ] Model metadata stored
- [ ] Database schema documented

### Engineering

- [ ] Modular code
- [ ] Type hints
- [ ] Error handling
- [ ] Logging
- [ ] Unit tests
- [ ] API tests
- [ ] Integration test
- [ ] Docker support

### Scientific work

- [ ] Research question defined
- [ ] Hypotheses/questions documented
- [ ] Methodology documented
- [ ] Experiments reproducible
- [ ] Results analyzed
- [ ] Limitations discussed
- [ ] Ethical considerations discussed
- [ ] Thesis written

---

# 41. Recommended Thesis Structure

## Chapter 1 — Introduction

- background;
- problem statement;
- motivation;
- objectives;
- research questions;
- contributions.

## Chapter 2 — Background

- cardiovascular risk prediction;
- machine learning;
- classification;
- web-based data systems;
- explainable AI.

## Chapter 3 — Related Work

Review relevant studies concerning:

- cardiovascular prediction;
- machine-learning methods;
- explainability;
- web-based predictive systems.

Do not merely list papers. Compare their methodologies and limitations.

## Chapter 4 — Dataset and Data Analysis

- dataset;
- features;
- target;
- data quality;
- EDA;
- limitations.

## Chapter 5 — Methodology

- preprocessing;
- feature engineering;
- models;
- hyperparameter optimization;
- validation strategy;
- evaluation metrics.

## Chapter 6 — System Design

- architecture;
- backend;
- database;
- frontend;
- API;
- model deployment.

## Chapter 7 — Experiments and Results

- baseline;
- model comparison;
- tuning;
- feature engineering;
- final evaluation;
- explainability.

## Chapter 8 — Discussion

- interpretation;
- comparison with related work;
- strengths;
- limitations;
- practical implications.

## Chapter 9 — Ethics and Limitations

- bias;
- privacy;
- dataset limitations;
- model uncertainty;
- medical-use limitations.

## Chapter 10 — Conclusion and Future Work

- answer research questions;
- summarize contribution;
- future improvements.

---

# 42. Suggested Hypotheses

If the thesis format requires hypotheses, possible hypotheses include:

### H1

> Ensemble-based machine-learning models can achieve different predictive performance from a linear baseline on the selected cardiovascular dataset.

### H2

> Feature engineering can change predictive performance compared with the original feature representation.

### H3

> Different machine-learning models produce different feature-importance patterns.

These hypotheses must be treated as questions to test, not assumptions that the results will confirm.

---

# 43. Optional Advanced Features

Only implement these after the core project is complete.

Possible extensions:

- model versioning;
- MLflow experiment tracking;
- calibration curves;
- probability calibration;
- SHAP interactive visualizations;
- batch prediction through CSV upload;
- data export;
- role-based access;
- asynchronous prediction jobs;
- CI/CD;
- GitHub Actions;
- automated Docker builds;
- cloud deployment.

Do not sacrifice the scientific thesis for unnecessary features.

---

# 44. What Should NOT Be Done

Avoid:

- training only one model;
- reporting only accuracy;
- randomly splitting data after preprocessing;
- data leakage;
- copying code from tutorials without understanding it;
- claiming the model is medically accurate;
- claiming feature importance proves causality;
- building a beautiful frontend while having weak experiments;
- adding technologies solely to make the project look impressive;
- using a huge dataset without understanding it;
- hiding failed experiments;
- reporting only the best result;
- fabricating results;
- omitting dataset limitations.

---

# 45. Minimum Viable Version

If time is limited, implement this first:

```text
Dataset
  ↓
EDA
  ↓
Preprocessing Pipeline
  ↓
5+ ML Models
  ↓
Cross-Validation
  ↓
Hyperparameter Tuning
  ↓
Final Evaluation
  ↓
Explainability
  ↓
FastAPI
  ↓
Database
  ↓
Simple Web Interface
```

Only after this works should you add Docker, advanced frontend features, CI/CD, or cloud deployment.

---

# 46. Stronger Version for a Competitive Application

To make the project particularly useful as evidence of preparation for a research-oriented master's programme, prioritize:

1. A clearly defined research question.
2. Reproducible experiments.
3. Careful prevention of data leakage.
4. Multiple model families.
5. Proper validation.
6. Interpretation of results rather than only reporting scores.
7. A well-designed data-intensive architecture.
8. A clean API.
9. A relational database.
10. Automated testing.
11. Strong academic writing.
12. Honest discussion of limitations.

The project should demonstrate that the student can move from:

```text
Problem
  ↓
Research Question
  ↓
Data
  ↓
Scientific Analysis
  ↓
Machine Learning
  ↓
Evaluation
  ↓
Interpretation
  ↓
Software Engineering
  ↓
Web/Data-Intensive System
  ↓
Scientific Conclusion
```

---

# 47. Curriculum Alignment — Web and Data-Intensive Systems Engineering

Modern academic curricula in Web and Data Science combine statistical machine-learning analysis with the design and development of web and data-intensive software systems. Key core competency areas include Machine Learning, Engineering Web & Data-Intensive Systems, Relational Data Modeling, REST API Design, and Software Quality Assurance.

This project is therefore deliberately designed to demonstrate several relevant dimensions simultaneously:

| Programme-relevant area | Project evidence |
|---|---|
| Programming | Python application and backend |
| Algorithms | ML algorithms and model comparison |
| Data Science | EDA, preprocessing, statistics, evaluation |
| Machine Learning | Multiple classification models |
| Web systems | Web application and REST API |
| Data-intensive systems | Database + prediction pipeline |
| Software engineering | Modular architecture, testing, validation |
| Academic work | Research question, methodology, experiments |
| Scientific writing | Full thesis |
| Visual analytics | Data and model visualizations |
| Pattern recognition | Classification task |
| Research readiness | Reproducibility and critical limitations |

This alignment should be described honestly in the thesis and application documents; the project should not claim to cover curriculum areas that it does not actually implement.

---

# 48. Final Deliverables

At the end of the project, the student should have:

```text
1. Source-code repository
2. Trained ML pipeline
3. Dataset documentation
4. Exploratory-analysis notebooks
5. Experimental results
6. Web application
7. REST API
8. Database
9. Automated tests
10. Docker configuration
11. Technical documentation
12. Academic thesis
13. Presentation slides
14. Demo
```

---

# 49. Final Project Positioning

The strongest way to present the project is not:

> "I developed a heart disease prediction website."

Instead:

> **"I conducted a comparative investigation of machine-learning approaches for cardiovascular risk prediction and designed a reproducible web-based data-intensive system for deploying, evaluating, and interpreting the resulting models."**

That description accurately reflects the intended combination of scientific investigation, data science, machine learning, software engineering, and Web/data-intensive development.

---

# 50. Important Academic Integrity Note

This specification is a project blueprint, not a replacement for independent scientific work.

The final thesis should contain:

- the student's own implementation;
- the student's own experiments;
- the student's own analysis;
- properly cited external sources;
- reproducible results.

All numerical results, conclusions, and claims must be generated and verified during the actual project.

