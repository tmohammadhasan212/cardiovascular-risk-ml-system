"""Unit and integration tests for modeling, evaluation, prediction, and SHAP explainability."""

import json
from pathlib import Path
import numpy as np
import pytest

from src.config import settings
from src.data.loading import get_train_test_split
from src.models.evaluate import compute_classification_metrics, compute_roc_curve_data
from src.models.interpret import ModelExplainer
from src.models.predict import PredictionEngine, get_prediction_engine


def test_pipeline_artifact_exists_and_loads():
    """Verify serialized pipeline artifact exists and can be loaded."""
    assert Path(settings.MODEL_PATH).exists()
    engine = PredictionEngine()
    assert engine.pipeline is not None
    assert "preprocessor" in engine.pipeline.named_steps
    assert "classifier" in engine.pipeline.named_steps


def test_metadata_completeness():
    """Verify metadata contains all required metrics, curves, and 7-model comparison."""
    assert Path(settings.METADATA_PATH).exists()
    with open(settings.METADATA_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    assert "model_name" in meta
    assert "model_version" in meta
    assert "test_metrics" in meta
    assert "model_comparison" in meta
    assert "roc_curve" in meta
    assert "global_importance" in meta

    # Verify all 7 model families were evaluated
    comparison = meta["model_comparison"]
    expected_models = [
        "Logistic Regression",
        "K-Nearest Neighbors",
        "Decision Tree",
        "Random Forest",
        "Support Vector Machine",
        "AdaBoost",
        "Gradient Boosting",
    ]
    for m in expected_models:
        assert m in comparison
        assert "cv_roc_auc_mean" in comparison[m]
        assert "cv_recall_mean" in comparison[m]


def test_compute_classification_metrics():
    """Verify metric computation accuracy, sensitivity, and specificity."""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 1, 0, 1])
    y_prob = np.array([0.1, 0.7, 0.4, 0.9])

    metrics = compute_classification_metrics(y_true, y_pred, y_prob)
    assert metrics["accuracy"] == 0.5
    assert metrics["precision"] == 0.5
    assert metrics["recall"] == 0.5
    assert metrics["specificity"] == 0.5
    assert metrics["confusion_matrix"]["tp"] == 1
    assert metrics["confusion_matrix"]["tn"] == 1
    assert metrics["confusion_matrix"]["fp"] == 1
    assert metrics["confusion_matrix"]["fn"] == 1
    assert metrics["roc_auc"] is not None


def test_prediction_engine_patient_inference():
    """Verify prediction, risk tiering, and SHAP attribution on clinical cases."""
    engine = get_prediction_engine()

    low_risk_sample = {
        "age": 35,
        "sex": 0,
        "cp": 0,
        "trestbps": 110,
        "chol": 170,
        "fbs": 0,
        "restecg": 0,
        "thalach": 180,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 0,
        "ca": 0,
        "thal": 1,
    }

    result = engine.predict_patient(low_risk_sample)
    assert "prediction" in result
    assert result["prediction"] in (0, 1)
    assert 0.0 <= result["probability"] <= 1.0
    assert result["risk_tier"] in ("Low Risk", "Moderate Risk", "High Risk")
    assert "feature_attributions" in result
    assert len(result["feature_attributions"]) > 0

    high_risk_sample = {
        "age": 67,
        "sex": 1,
        "cp": 3,
        "trestbps": 160,
        "chol": 286,
        "fbs": 1,
        "restecg": 2,
        "thalach": 108,
        "exang": 1,
        "oldpeak": 3.5,
        "slope": 2,
        "ca": 3,
        "thal": 3,
    }

    result_high = engine.predict_patient(high_risk_sample)
    assert result_high["probability"] > result["probability"]
    assert result_high["risk_tier"] in ("Moderate Risk", "High Risk")


def test_model_explainer_global_and_local():
    """Verify SHAP explainer runs on background data and computes attributions."""
    X_train, _, _, _ = get_train_test_split()
    engine = get_prediction_engine()
    explainer = ModelExplainer(engine.pipeline, X_train.iloc[:30])

    global_imp = explainer.get_global_importance(top_n=5)
    assert isinstance(global_imp, list)
    assert len(global_imp) == 5
    assert "feature" in global_imp[0]
    assert "importance" in global_imp[0]
