"""Model interpretability module utilizing SHAP and feature importance techniques.

Supports both dataset-wide global explanations and single-patient local attributions.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
import shap
from sklearn.pipeline import Pipeline

from src.config import settings
from src.data.preprocessing import get_feature_names


class ModelExplainer:
    """Explainer using SHAP for global and local model interpretation."""

    def __init__(self, pipeline: Pipeline, background_data: pd.DataFrame):
        self.pipeline = pipeline
        self.preprocessor = pipeline.named_steps["preprocessor"]
        self.model = pipeline.named_steps["classifier"]
        self.background_raw = background_data
        
        # Transform background data for SHAP explainer
        self.background_transformed = self.preprocessor.transform(background_data)
        self.feature_names = get_feature_names(self.preprocessor)
        
        # Initialize SHAP explainer
        self._init_explainer()

    def _init_explainer(self):
        """Select the most suitable SHAP explainer depending on model family."""
        model_name = self.model.__class__.__name__
        try:
            if "Forest" in model_name or "Boosting" in model_name or "Tree" in model_name:
                self.explainer = shap.TreeExplainer(self.model)
                self.explainer_type = "tree"
            elif "LogisticRegression" in model_name:
                self.explainer = shap.LinearExplainer(
                    self.model, self.background_transformed
                )
                self.explainer_type = "linear"
            else:
                # KernelExplainer on a medoid sample of background data for speed
                bg_sample = shap.sample(self.background_transformed, 30, random_state=42)
                self.explainer = shap.KernelExplainer(
                    lambda x: self.model.predict_proba(x)[:, 1], bg_sample
                )
                self.explainer_type = "kernel"
        except Exception:
            # Fallback to general KernelExplainer on small sample
            bg_sample = shap.sample(self.background_transformed, 20, random_state=42)
            self.explainer = shap.KernelExplainer(
                lambda x: self.model.predict_proba(x)[:, 1], bg_sample
            )
            self.explainer_type = "kernel_fallback"

    def get_global_importance(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Calculate global mean absolute SHAP values across background dataset."""
        try:
            shap_values = self.explainer.shap_values(self.background_transformed)
            # Handle different SHAP output formats (list for binary classes vs single array)
            if isinstance(shap_values, list):
                # Typically index 1 corresponds to positive class
                values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
            elif isinstance(shap_values, np.ndarray) and len(shap_values.shape) == 3:
                values = shap_values[:, :, 1]
            else:
                values = shap_values

            mean_abs = np.mean(np.abs(values), axis=0)
            ranking = []
            for name, score in zip(self.feature_names, mean_abs):
                ranking.append({"feature": name, "importance": round(float(score), 4)})

            ranking = sorted(ranking, key=lambda x: x["importance"], reverse=True)
            return ranking[:top_n]
        except Exception:
            # Fallback to feature_importances_ if available on classifier
            if hasattr(self.model, "feature_importances_"):
                importances = self.model.feature_importances_
                ranking = [
                    {"feature": name, "importance": round(float(score), 4)}
                    for name, score in zip(self.feature_names, importances)
                ]
                return sorted(ranking, key=lambda x: x["importance"], reverse=True)[:top_n]
            return []

    def explain_patient(
        self, patient_dict: Dict[str, Any], top_n: int = 8
    ) -> List[Dict[str, Any]]:
        """Explain a single patient prediction with directional SHAP contributions.
        
        Returns a list of contributing features, the patient's raw value, and whether
        it pushes risk higher (+ SHAP) or lowers risk (- SHAP).
        """
        # Ensure DataFrame with standard feature columns
        df_patient = pd.DataFrame([patient_dict])[settings.ALL_FEATURE_COLUMNS]
        X_trans = self.preprocessor.transform(df_patient)

        try:
            shap_vals = self.explainer.shap_values(X_trans)
            if isinstance(shap_vals, list):
                vals = shap_vals[1][0] if len(shap_vals) > 1 else shap_vals[0][0]
            elif isinstance(shap_vals, np.ndarray) and len(shap_vals.shape) == 3:
                vals = shap_vals[0, :, 1]
            elif isinstance(shap_vals, np.ndarray) and len(shap_vals.shape) == 2:
                vals = shap_vals[0]
            else:
                vals = np.array(shap_vals)

            contributions = []
            for feat_name, shap_val in zip(self.feature_names, vals):
                # Map one-hot or raw feature back to patient field where possible
                base_feat = feat_name.split("_")[0] if "_" in feat_name else feat_name
                raw_val = patient_dict.get(base_feat, patient_dict.get(feat_name, None))

                direction = "increases_risk" if shap_val > 0 else "decreases_risk"
                contributions.append(
                    {
                        "feature": feat_name,
                        "base_feature": base_feat,
                        "patient_value": raw_val,
                        "attribution": round(float(shap_val), 4),
                        "abs_attribution": round(abs(float(shap_val)), 4),
                        "direction": direction,
                    }
                )

            # Sort by highest absolute impact
            contributions = sorted(
                contributions, key=lambda x: x["abs_attribution"], reverse=True
            )
            return contributions[:top_n]

        except Exception as e:
            # Defensive fallback
            return [
                {
                    "feature": "Assessment",
                    "base_feature": "model",
                    "patient_value": "standard",
                    "attribution": 0.0,
                    "abs_attribution": 0.0,
                    "direction": "neutral",
                    "note": f"SHAP explanation fallback: {str(e)}",
                }
            ]
