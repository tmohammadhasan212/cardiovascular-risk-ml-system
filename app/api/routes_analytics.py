"""FastAPI router for model metadata, 7-algorithm comparison, and research analytics."""

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, status

from src.config import settings

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics & Research"])


def load_metadata_cached():
    """Load model evaluation metadata JSON from disk."""
    if not Path(settings.METADATA_PATH).exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model metadata not found. Train the model pipeline first.",
        )
    with open(settings.METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get(
    "/model-info",
    status_code=status.HTTP_200_OK,
    summary="Get active model metadata and test set metrics",
)
def get_model_info():
    meta = load_metadata_cached()
    return {
        "model_name": meta.get("model_name"),
        "model_version": meta.get("model_version"),
        "trained_at": meta.get("trained_at"),
        "training_samples": meta.get("training_samples"),
        "test_samples": meta.get("test_samples"),
        "best_hyperparameters": meta.get("best_hyperparameters"),
        "best_cv_roc_auc": meta.get("best_cv_roc_auc"),
        "test_metrics": meta.get("test_metrics"),
        "features": meta.get("features"),
    }


@router.get(
    "/model-comparison",
    status_code=status.HTTP_200_OK,
    summary="Get cross-validation comparison across all 7 evaluated algorithms",
)
def get_model_comparison():
    meta = load_metadata_cached()
    return meta.get("model_comparison", {})


@router.get(
    "/global-importance",
    status_code=status.HTTP_200_OK,
    summary="Get global feature importance values from SHAP",
)
def get_global_importance():
    meta = load_metadata_cached()
    return meta.get("global_importance", [])


@router.get(
    "/curves",
    status_code=status.HTTP_200_OK,
    summary="Get ROC curve and Precision-Recall curve coordinates",
)
def get_evaluation_curves():
    meta = load_metadata_cached()
    return {
        "roc_curve": meta.get("roc_curve", {}),
        "pr_curve": meta.get("pr_curve", {}),
    }
