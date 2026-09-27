"""Model evaluation module computing classification metrics and curves."""

from typing import Any, Dict, List, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """Calculate comprehensive classification evaluation metrics.
    
    Includes Accuracy, Precision, Recall (Sensitivity), Specificity,
    F1-score, ROC-AUC, and Confusion Matrix.
    """
    cm = confusion_matrix(y_true, y_pred)
    # Extract TN, FP, FN, TP safely
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0
    else:
        tn, fp, fn, tp = 0, 0, 0, 0
        specificity = 0.0

    metrics: Dict[str, Any] = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "sensitivity": float(recall_score(y_true, y_pred, zero_division=0)),
        "specificity": specificity,
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
    }

    if y_prob is not None:
        try:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
        except Exception:
            metrics["roc_auc"] = None
    else:
        metrics["roc_auc"] = None

    return metrics


def compute_roc_curve_data(
    y_true: np.ndarray,
    y_prob: np.ndarray,
) -> Dict[str, List[float]]:
    """Generate ROC curve coordinates (False Positive Rate and True Positive Rate)."""
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    clean_thresholds = [
        1.0 if np.isinf(x) else round(float(x), 4) for x in thresholds
    ]
    return {
        "fpr": [round(float(x), 4) for x in fpr],
        "tpr": [round(float(x), 4) for x in tpr],
        "thresholds": clean_thresholds,
    }


def compute_pr_curve_data(
    y_true: np.ndarray,
    y_prob: np.ndarray,
) -> Dict[str, List[float]]:
    """Generate Precision-Recall curve coordinates."""
    precision, recall, thresholds = precision_recall_curve(y_true, y_prob)
    return {
        "precision": [round(float(x), 4) for x in precision],
        "recall": [round(float(x), 4) for x in recall],
        "thresholds": [round(float(x), 4) for x in thresholds],
    }
