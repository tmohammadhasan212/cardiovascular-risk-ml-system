# REST API Specification

The **Cardiovascular Risk Prediction & Analysis API** is implemented in FastAPI.

Base URL: `http://localhost:8000`  
Interactive Swagger UI: `http://localhost:8000/docs`  
ReDoc Documentation: `http://localhost:8000/redoc`

---

## 1. Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check service health, model loading state, and DB connectivity. |
| `POST` | `/api/v1/predict` | Predict cardiovascular risk for a patient and generate SHAP attributions. |
| `POST` | `/api/v1/predict/batch` | Concurrently evaluate an array of patient records. |
| `GET` | `/api/v1/history` | Query paginated assessment history with optional risk tier filtering. |
| `GET` | `/api/v1/history/stats` | Retrieve aggregate counts and mean risk score across all assessments. |
| `GET` | `/api/v1/history/{id}` | Retrieve single prediction record by ID. |
| `DELETE` | `/api/v1/history/{id}` | Delete prediction record by ID. |
| `GET` | `/api/v1/history/export/csv` | Download complete prediction history as CSV. |
| `GET` | `/api/v1/analytics/model-info` | Retrieve active model hyperparameters, version, and test metrics. |
| `GET` | `/api/v1/analytics/model-comparison` | Retrieve 7-algorithm cross-validation evaluation table. |
| `GET` | `/api/v1/analytics/global-importance` | Retrieve global SHAP feature importance rankings. |
| `GET` | `/api/v1/analytics/curves` | Retrieve ROC curve and PR curve plotting coordinates. |

---

## 2. Endpoint Details & Examples

### `GET /health`
Verifies operational readiness.

#### Response `200 OK`
```json
{
  "status": "ok",
  "model_loaded": true,
  "database_connected": true,
  "version": "1.0.0"
}
```

---

### `POST /api/v1/predict`
Calculates cardiovascular risk and generates local SHAP feature attributions.

#### Request Body
```json
{
  "age": 60,
  "sex": 1,
  "cp": 2,
  "trestbps": 140.0,
  "chol": 240.0,
  "fbs": 0,
  "restecg": 1,
  "thalach": 145.0,
  "exang": 1,
  "oldpeak": 1.8,
  "slope": 1,
  "ca": 1,
  "thal": 2
}
```

#### Response `200 OK`
```json
{
  "id": 1,
  "prediction": 1,
  "probability": 0.6763,
  "risk_tier": "High Risk",
  "model_version": "1.0.0",
  "model_name": "Logistic Regression",
  "feature_attributions": [
    {
      "feature": "ca",
      "base_feature": "ca",
      "patient_value": 1,
      "attribution": 0.3604,
      "abs_attribution": 0.3604,
      "direction": "increases_risk"
    },
    {
      "feature": "oldpeak",
      "base_feature": "oldpeak",
      "patient_value": 1.8,
      "attribution": 0.1892,
      "abs_attribution": 0.1892,
      "direction": "increases_risk"
    }
  ],
  "created_at": "2026-09-27T15:20:19.676504",
  "disclaimer": "Academic machine-learning prototype for scientific evaluation. Not intended for clinical diagnosis or medical decision-making."
}
```

---

### `GET /api/v1/history`
Returns paginated prediction history.

#### Query Parameters
- `skip` (int, default=0): Offset for pagination.
- `limit` (int, default=50, max=200): Records to return.
- `risk_tier` (string, optional): Filter by `Low Risk`, `Moderate Risk`, or `High Risk`.

#### Response `200 OK`
```json
{
  "total": 1,
  "items": [
    {
      "id": 1,
      "created_at": "2026-09-27T15:20:19.676504",
      "patient_data": {
        "age": 60,
        "sex": 1,
        "cp": 2,
        "trestbps": 140.0,
        "chol": 240.0,
        "fbs": 0,
        "restecg": 1,
        "thalach": 145.0,
        "exang": 1,
        "oldpeak": 1.8,
        "slope": 1,
        "ca": 1,
        "thal": 2
      },
      "prediction": 1,
      "probability": 0.6763,
      "risk_tier": "High Risk",
      "model_version": "1.0.0"
    }
  ],
  "skip": 0,
  "limit": 50
}
```

---

### `GET /api/v1/analytics/model-comparison`
Returns cross-validation performance across all 7 evaluated machine learning algorithms.

#### Response `200 OK`
```json
{
  "Logistic Regression": {
    "cv_accuracy_mean": 0.843,
    "cv_accuracy_std": 0.025,
    "cv_precision_mean": 0.8387,
    "cv_recall_mean": 0.8378,
    "cv_f1_mean": 0.8335,
    "cv_roc_auc_mean": 0.9117,
    "cv_roc_auc_std": 0.021
  },
  "Random Forest": {
    "cv_accuracy_mean": 0.8142,
    "cv_accuracy_std": 0.034,
    "cv_precision_mean": 0.8089,
    "cv_recall_mean": 0.7838,
    "cv_f1_mean": 0.7916,
    "cv_roc_auc_mean": 0.8943,
    "cv_roc_auc_std": 0.028
  }
}
```
