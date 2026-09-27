# System Architecture Document

## 1. Executive Architecture Overview

The **Cardiovascular Risk Machine Learning System** is engineered as a decoupled, reproducible, data-intensive web system developed as a final Bachelor's graduation project.

The system integrates four distinct subsystems:
1. **Machine Learning & Feature Pipeline Subsystem**: Offline reproducible pipeline handling data ingestion, stratified leakage-free preprocessing, 7-model training, hyperparameter optimization, and SHAP explainability.
2. **Persistence Subsystem**: Relational database (SQLAlchemy ORM) supporting dual modes: SQLite (zero-setup for development) and PostgreSQL (production).
3. **Application & REST API Subsystem**: Asynchronous FastAPI service delivering strict schema validation (Pydantic v2), inference orchestration, history querying, and research analytics.
4. **Client-Side Presentation Subsystem**: Modern responsive single-page dashboard featuring clinical parameter forms, animated radial risk gauges, directional SHAP attribution charts, and research analytics.

---

## 2. High-Level Architecture Diagram

```mermaid
flowchart TD
    subgraph Client ["Client Presentation Tier (Browser)"]
        UI["Web Dashboard (Vanilla JS / CSS3 / HTML5)"]
        Form["Patient Input Form with Presets"]
        Gauge["SVG Radial Risk Gauge"]
        ShapUI["Local SHAP Attribution Visualizer"]
        HistUI["Persistent History Table & CSV Exporter"]
        ResearchUI["Comparative Model Analytics Dashboard"]
    end

    subgraph API ["Application Tier (FastAPI Engine)"]
        Main["FastAPI Gateway (app.main:app)"]
        PredRoute["/api/v1/predict"]
        HistRoute["/api/v1/history"]
        AnalyticsRoute["/api/v1/analytics"]
        PredService["Prediction Service (Inference Orchestrator)"]
    end

    subgraph ML ["Machine Learning Tier (Joblib & SHAP)"]
        Pipeline["Serialized Pipeline (models/best_model.joblib)"]
        Preproc["ColumnTransformer (Imputer + Scaler + Encoder)"]
        Model["Tuned Classifier (Logistic Regression / Ensembles)"]
        Explainer["SHAP Explainer Engine (Linear / Tree / Kernel)"]
        Metadata["Evaluation Metadata (models/model_metadata.json)"]
    end

    subgraph Data ["Data Persistence Tier (SQLAlchemy ORM)"]
        DB[(SQL Database<br/>SQLite / PostgreSQL)]
        PredRecord["Table: prediction_records"]
        ModelVer["Table: model_versions"]
    end

    Form -->|POST /api/v1/predict| PredRoute
    HistUI -->|GET /api/v1/history| HistRoute
    HistUI -->|GET /export/csv| HistRoute
    ResearchUI -->|GET /api/v1/analytics/*| AnalyticsRoute

    PredRoute --> PredService
    PredService --> Pipeline
    Pipeline --> Preproc
    Preproc --> Model
    PredService --> Explainer
    PredService --> DB

    HistRoute --> DB
    AnalyticsRoute --> Metadata

    PredRoute -->|JSON Prediction + Attributions| Gauge
    PredRoute -->|JSON Local SHAP| ShapUI
    DB --> HistUI
    Metadata --> ResearchUI
```

---

## 3. Database Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    PREDICTION_RECORD {
        int id PK "Autoincrementing Identifier"
        datetime created_at "Assessment Timestamp (UTC)"
        int age "Patient Age (years)"
        int sex "Biological Sex (1=M, 0=F)"
        int cp "Chest Pain Category (0-3)"
        float trestbps "Resting Blood Pressure (mm Hg)"
        float chol "Serum Cholesterol (mg/dl)"
        int fbs "Fasting Blood Sugar > 120 (1/0)"
        int restecg "Resting ECG Category (0-2)"
        float thalach "Maximum Heart Rate Achieved (bpm)"
        int exang "Exercise Induced Angina (1/0)"
        float oldpeak "ST Depression Relative to Rest (mm)"
        int slope "Slope of Peak Exercise ST Segment (0-2)"
        int ca "Fluoroscopy Major Vessels (0-3)"
        int thal "Thalassemia Scan Condition (1-3)"
        int prediction "Model Binary Prediction (0/1)"
        float probability "Predicted Probability of Disease [0,1]"
        string risk_tier "Risk Classification (Low/Moderate/High)"
        text top_features "JSON Array of Local SHAP Attributions"
        string model_version "Deployed Pipeline Identifier"
    }

    MODEL_VERSION {
        int id PK "Autoincrementing Identifier"
        string version "Semantic Version (e.g. 1.0.0)"
        string model_name "Algorithm Family Name"
        datetime training_date "Training Execution Timestamp"
        string dataset_version "Dataset Provenance Identifier"
        text metrics "JSON Object with Test & CV Performance"
        boolean is_active "Active Serving Flag"
    }
```

---

## 4. End-to-End Prediction & Explainability Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as Clinician / Researcher
    participant UI as Web Dashboard
    participant API as FastAPI Router
    participant Service as Prediction Service
    participant Model as Pipeline (.joblib)
    participant SHAP as Model Explainer
    participant DB as SQL Database

    User->>UI: Enter patient vitals or select sample profile
    User->>UI: Click "Calculate Cardiovascular Risk"
    UI->>API: POST /api/v1/predict (JSON payload)
    API->>API: Validate against PatientInputSchema (Pydantic v2)
    API->>Service: process_patient_prediction(patient_input)
    Service->>Model: pipeline.predict_proba(patient_df)
    Model-->>Service: probability = 0.334, prediction = 0
    Service->>Service: Calculate risk tier ("Low Risk")
    Service->>SHAP: explainer.explain_patient(patient_dict)
    SHAP-->>Service: Feature attributions list [ca: -0.44, thalach: -0.25, ...]
    Service->>DB: INSERT INTO prediction_records (...)
    DB-->>Service: record_id = 42
    Service-->>API: Structured result payload
    API-->>UI: HTTP 200 OK (prediction, probability, risk_tier, SHAP attributions)
    UI->>UI: Animate radial gauge to 33% (Green)
    UI->>UI: Render directional waterfall bars (Protective vs. Risk)
```

---

## 5. Technology Stack Rationale

| Layer | Chosen Technology | Architectural Justification |
|---|---|---|
| **Runtime** | Python 3.12 | Modern type-hinting support, native performance optimizations, long-term support. |
| **Data Processing** | NumPy & pandas | Standard high-performance vectorized operations on tabular clinical structures. |
| **Machine Learning** | scikit-learn | Strict API standard, zero data leakage with `Pipeline` and `ColumnTransformer`, built-in cross-validation and hyperparameter search. |
| **Model Explainability** | SHAP (Shapley Additive exPlanations) | Game-theoretic foundation ensuring local accuracy, missingness, and consistency properties. |
| **Web API Framework** | FastAPI & Uvicorn | Native async support, high throughput, automatic OpenAPI specification generation, dependency injection. |
| **Data Validation** | Pydantic v2 | High-speed Rust-based input validation with clear clinical range constraints. |
| **Persistence / ORM** | SQLAlchemy 2.0 | Decoupled database engine supporting SQLite for rapid local runs and PostgreSQL for enterprise containers. |
| **Containerization** | Docker & Compose | Guarantees 100% environment reproducibility across Linux, macOS, and Windows. |
