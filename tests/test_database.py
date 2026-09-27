"""Unit tests for SQLAlchemy database models, repository operations, and statistics."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.connection import Base
from app.database.models import PredictionRecord
from app.database.repository import PredictionRepository


@pytest.fixture
def db_session():
    """In-memory SQLite database session fixture for isolated testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_create_and_retrieve_prediction(db_session):
    """Test saving a prediction record and retrieving it."""
    patient_data = {
        "age": 55,
        "sex": 1,
        "cp": 2,
        "trestbps": 130.0,
        "chol": 220.0,
        "fbs": 0,
        "restecg": 1,
        "thalach": 160.0,
        "exang": 0,
        "oldpeak": 0.5,
        "slope": 1,
        "ca": 0,
        "thal": 2,
    }
    prediction_result = {
        "prediction": 0,
        "probability": 0.28,
        "risk_tier": "Low Risk",
        "model_version": "1.0.0",
        "feature_attributions": [
            {
                "feature": "thalach",
                "base_feature": "thalach",
                "patient_value": 160.0,
                "attribution": -0.25,
                "abs_attribution": 0.25,
                "direction": "decreases_risk",
            }
        ],
    }

    record = PredictionRepository.create_prediction(
        db_session, patient_data, prediction_result
    )
    assert record.id is not None
    assert record.age == 55
    assert record.prediction == 0
    assert record.risk_tier == "Low Risk"

    # Query back
    fetched = PredictionRepository.get_prediction_by_id(db_session, record.id)
    assert fetched is not None
    assert fetched.probability == 0.28


def test_get_history_and_filtering(db_session):
    """Test history querying with pagination and risk filtering."""
    sample_base = {
        "age": 50,
        "sex": 1,
        "cp": 1,
        "trestbps": 120.0,
        "chol": 200.0,
        "fbs": 0,
        "restecg": 0,
        "thalach": 150.0,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 0,
        "ca": 0,
        "thal": 1,
    }

    # Insert 1 Low Risk and 2 High Risk
    PredictionRepository.create_prediction(
        db_session,
        sample_base,
        {"prediction": 0, "probability": 0.20, "risk_tier": "Low Risk", "model_version": "1.0.0"},
    )
    PredictionRepository.create_prediction(
        db_session,
        sample_base,
        {"prediction": 1, "probability": 0.85, "risk_tier": "High Risk", "model_version": "1.0.0"},
    )
    PredictionRepository.create_prediction(
        db_session,
        sample_base,
        {"prediction": 1, "probability": 0.90, "risk_tier": "High Risk", "model_version": "1.0.0"},
    )

    all_records = PredictionRepository.get_history(db_session, limit=10)
    assert len(all_records) == 3

    high_records = PredictionRepository.get_history(
        db_session, risk_filter="High Risk"
    )
    assert len(high_records) == 2

    low_records = PredictionRepository.get_history(
        db_session, risk_filter="Low Risk"
    )
    assert len(low_records) == 1


def test_delete_prediction_and_stats(db_session):
    """Test deleting records and calculating summary statistics."""
    sample_base = {
        "age": 60,
        "sex": 0,
        "cp": 2,
        "trestbps": 140.0,
        "chol": 250.0,
        "fbs": 0,
        "restecg": 1,
        "thalach": 140.0,
        "exang": 1,
        "oldpeak": 1.5,
        "slope": 1,
        "ca": 1,
        "thal": 2,
    }

    rec = PredictionRepository.create_prediction(
        db_session,
        sample_base,
        {"prediction": 1, "probability": 0.70, "risk_tier": "High Risk", "model_version": "1.0.0"},
    )

    stats = PredictionRepository.get_history_summary_statistics(db_session)
    assert stats["total_assessments"] == 1
    assert stats["high_risk_count"] == 1
    assert stats["average_predicted_risk"] == 0.70

    # Delete record
    success = PredictionRepository.delete_prediction(db_session, rec.id)
    assert success is True

    # Check that record is gone
    assert PredictionRepository.get_prediction_by_id(db_session, rec.id) is None
    assert PredictionRepository.get_total_count(db_session) == 0
