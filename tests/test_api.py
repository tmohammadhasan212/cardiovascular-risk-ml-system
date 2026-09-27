"""Unit and functional tests for FastAPI endpoints, input validation, and history flows."""

import pytest


def test_health_endpoint(client):
    """Verify healthcheck endpoint response."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_loaded"] is True
    assert data["database_connected"] is True


def test_index_dashboard_view(client):
    """Verify HTML single-page dashboard renders with form and controls."""
    response = client.get("/")
    assert response.status_code == 200
    assert "CardioPredict ML" in response.text
    assert "patient-form" in response.text


def test_predict_patient_valid(client):
    """Verify valid patient prediction returns probabilities, risk tier, and explanations."""
    payload = {
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
        "thal": 2,
    }

    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "prediction" in data
    assert data["prediction"] in (0, 1)
    assert 0.0 <= data["probability"] <= 1.0
    assert data["risk_tier"] in ("Low Risk", "Moderate Risk", "High Risk")
    assert isinstance(data["feature_attributions"], list)
    assert len(data["feature_attributions"]) > 0
    assert data["id"] is not None


def test_predict_patient_invalid_ranges(client):
    """Verify that clinical boundary violations trigger 422 Unprocessable Entity."""
    payload = {
        "age": 150,
        "sex": 1,
        "cp": 2,
        "trestbps": -50.0,
        "chol": 240.0,
        "fbs": 0,
        "restecg": 1,
        "thalach": 145.0,
        "exang": 0,
        "oldpeak": 1.0,
        "slope": 1,
        "ca": 0,
        "thal": 2,
    }

    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_batch_prediction(client):
    """Verify batch prediction endpoint evaluates multiple patient records."""
    patients = [
        {
            "age": 45,
            "sex": 0,
            "cp": 1,
            "trestbps": 120.0,
            "chol": 190.0,
            "fbs": 0,
            "restecg": 0,
            "thalach": 170.0,
            "exang": 0,
            "oldpeak": 0.0,
            "slope": 0,
            "ca": 0,
            "thal": 1,
        },
        {
            "age": 68,
            "sex": 1,
            "cp": 3,
            "trestbps": 165.0,
            "chol": 290.0,
            "fbs": 1,
            "restecg": 2,
            "thalach": 110.0,
            "exang": 1,
            "oldpeak": 3.0,
            "slope": 2,
            "ca": 2,
            "thal": 3,
        },
    ]

    response = client.post("/api/v1/predict/batch", json=patients)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["probability"] < data[1]["probability"]


def test_history_flow_and_export(client):
    """Verify prediction creation, history pagination, single record lookup, and CSV export."""
    payload = {
        "age": 52,
        "sex": 1,
        "cp": 0,
        "trestbps": 125.0,
        "chol": 210.0,
        "fbs": 0,
        "restecg": 0,
        "thalach": 165.0,
        "exang": 0,
        "oldpeak": 0.2,
        "slope": 0,
        "ca": 0,
        "thal": 1,
    }

    post_resp = client.post("/api/v1/predict", json=payload)
    assert post_resp.status_code == 200
    record_id = post_resp.json()["id"]

    # History list
    hist_resp = client.get("/api/v1/history")
    assert hist_resp.status_code == 200
    assert hist_resp.json()["total"] == 1

    # Single lookup
    get_resp = client.get(f"/api/v1/history/{record_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["patient_data"]["age"] == 52

    # CSV Export
    csv_resp = client.get("/api/v1/history/export/csv")
    assert csv_resp.status_code == 200
    assert "text/csv" in csv_resp.headers["content-type"]
    assert "age,sex,cp" in csv_resp.text

    # Delete record
    del_resp = client.delete(f"/api/v1/history/{record_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["success"] is True


def test_analytics_endpoints(client):
    """Verify model-info, comparison, and global importance research endpoints."""
    # Model info
    resp = client.get("/api/v1/analytics/model-info")
    assert resp.status_code == 200
    assert "model_name" in resp.json()
    assert "test_metrics" in resp.json()

    # Model comparison
    comp_resp = client.get("/api/v1/analytics/model-comparison")
    assert comp_resp.status_code == 200
    comp_data = comp_resp.json()
    assert len(comp_data) >= 7

    # Global SHAP importance
    imp_resp = client.get("/api/v1/analytics/global-importance")
    assert imp_resp.status_code == 200
    assert isinstance(imp_resp.json(), list)

    # Evaluation curves
    curves_resp = client.get("/api/v1/analytics/curves")
    assert curves_resp.status_code == 200
    assert "roc_curve" in curves_resp.json()
    assert "pr_curve" in curves_resp.json()
