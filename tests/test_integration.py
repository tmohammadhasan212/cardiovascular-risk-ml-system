"""End-to-end integration tests verifying the complete clinical workflow and persistence."""

import pytest


def test_full_clinical_lifecycle(client):
    """Verify complete end-to-end user journey across all system components."""
    # 1. Healthcheck
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    # 2. Inspect Model Information & 7-Model Comparison
    analytics = client.get("/api/v1/analytics/model-comparison")
    assert analytics.status_code == 200
    models = analytics.json()
    assert len(models) >= 7
    assert "Logistic Regression" in models
    assert "Random Forest" in models

    # 3. Assess Low Risk Patient
    low_risk_patient = {
        "age": 36,
        "sex": 0,
        "cp": 0,
        "trestbps": 115.0,
        "chol": 175.0,
        "fbs": 0,
        "restecg": 0,
        "thalach": 178.0,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 0,
        "ca": 0,
        "thal": 1,
    }
    low_res = client.post("/api/v1/predict", json=low_risk_patient)
    assert low_res.status_code == 200
    low_data = low_res.json()
    assert low_data["prediction"] == 0
    assert low_data["risk_tier"] == "Low Risk"
    assert low_data["probability"] < 0.35
    assert len(low_data["feature_attributions"]) > 0
    low_id = low_data["id"]

    # 4. Assess High Risk Patient
    high_risk_patient = {
        "age": 67,
        "sex": 1,
        "cp": 3,
        "trestbps": 160.0,
        "chol": 286.0,
        "fbs": 1,
        "restecg": 2,
        "thalach": 108.0,
        "exang": 1,
        "oldpeak": 3.2,
        "slope": 2,
        "ca": 2,
        "thal": 3,
    }
    high_res = client.post("/api/v1/predict", json=high_risk_patient)
    assert high_res.status_code == 200
    high_data = high_res.json()
    assert high_data["prediction"] == 1
    assert high_data["risk_tier"] == "High Risk"
    assert high_data["probability"] > 0.65
    high_id = high_data["id"]

    # 5. Check History List
    history = client.get("/api/v1/history")
    assert history.status_code == 200
    history_items = history.json()["items"]
    assert len(history_items) == 2
    assert history.json()["total"] == 2

    # 6. Check Aggregate History Statistics
    stats = client.get("/api/v1/history/stats")
    assert stats.status_code == 200
    stats_data = stats.json()
    assert stats_data["total_assessments"] == 2
    assert stats_data["low_risk_count"] == 1
    assert stats_data["high_risk_count"] == 1

    # 7. Export Records to CSV
    csv_export = client.get("/api/v1/history/export/csv")
    assert csv_export.status_code == 200
    csv_text = csv_export.text
    assert "Low Risk" in csv_text
    assert "High Risk" in csv_text

    # 8. Delete One Record & Verify Update
    del_res = client.delete(f"/api/v1/history/{low_id}")
    assert del_res.status_code == 200

    updated_history = client.get("/api/v1/history")
    assert updated_history.json()["total"] == 1
    remaining_ids = [item["id"] for item in updated_history.json()["items"]]
    assert low_id not in remaining_ids
    assert high_id in remaining_ids
