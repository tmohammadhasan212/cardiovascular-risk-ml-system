"""Inference and risk classification service with integrated explanation generation."""

import json
from pathlib import Path
from typing import Any, Dict, Optional
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.config import settings
from src.data.loading import get_train_test_split
from src.models.interpret import ModelExplainer


class PredictionEngine:
    """Singleton-style inference engine managing the trained pipeline and SHAP explainer."""

    def __init__(
        self,
        model_path: Optional[Path] = None,
        metadata_path: Optional[Path] = None,
    ):
        self.model_path = model_path or settings.MODEL_PATH
        self.metadata_path = metadata_path or settings.METADATA_PATH
        self.pipeline: Optional[Pipeline] = None
        self.metadata: Optional[Dict[str, Any]] = None
        self.explainer: Optional[ModelExplainer] = None

        self.load()

    def load(self):
        """Load pipeline artifact, metadata, and initialize explainer."""
        if not Path(self.model_path).exists():
            raise FileNotFoundError(
                f"Model artifact not found at {self.model_path}. Run 'python -m src.models.train' first."
            )

        self.pipeline = joblib.load(self.model_path)

        if Path(self.metadata_path).exists():
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "model_name": self.pipeline.named_steps["classifier"].__class__.__name__,
                "model_version": settings.APP_VERSION,
            }

        # Initialize explainer using training partition
        try:
            X_train, _, _, _ = get_train_test_split()
            self.explainer = ModelExplainer(self.pipeline, X_train)
        except Exception as e:
            print(f"Warning: Explainer initialization deferred or failed: {e}")
            self.explainer = None

    def predict_patient(self, patient_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Perform cardiovascular risk prediction and generate SHAP attributions."""
        if self.pipeline is None:
            raise RuntimeError("Pipeline is not loaded.")

        # Ensure DataFrame formatted according to training schema
        df = pd.DataFrame([patient_dict])[settings.ALL_FEATURE_COLUMNS]

        prob = float(self.pipeline.predict_proba(df)[0, 1])
        pred = int(self.pipeline.predict(df)[0])

        # Stratify risk tier based on clinical thresholds
        if prob < 0.35:
            risk_tier = "Low Risk"
        elif prob < 0.65:
            risk_tier = "Moderate Risk"
        else:
            risk_tier = "High Risk"

        # Generate local attributions
        if self.explainer:
            attributions = self.explainer.explain_patient(patient_dict, top_n=6)
        else:
            attributions = []

        return {
            "prediction": pred,
            "probability": round(prob, 4),
            "risk_tier": risk_tier,
            "model_version": self.metadata.get("model_version", settings.APP_VERSION),
            "model_name": self.metadata.get("model_name", "Cardiovascular ML Model"),
            "feature_attributions": attributions,
            "disclaimer": (
                "Academic machine-learning prototype for research demonstration. "
                "Not intended for medical diagnosis or clinical decision-making."
            ),
        }


# Global singleton instance for the application
prediction_engine: Optional[PredictionEngine] = None


def get_prediction_engine() -> PredictionEngine:
    """Retrieve or initialize the global PredictionEngine instance."""
    global prediction_engine
    if prediction_engine is None:
        prediction_engine = PredictionEngine()
    return prediction_engine
