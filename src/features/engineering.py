"""Feature engineering module with clinically motivated transformations.

Implemented as a scikit-learn compatible Transformer to prevent data leakage.
"""

from typing import List
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ClinicalFeatureEngineer(BaseEstimator, TransformerMixin):
    """Generates clinically interpretable derived features.
    
    Transformations:
    - hr_max_ratio: thalach / (220 - age) (fraction of age-predicted maximum heart rate)
    - bp_chol_product: (trestbps * chol) / 1000 (combined hemodynamic-lipid stress index)
    - exang_oldpeak_interaction: exang * oldpeak (ischemia severity index)
    - age_risk_flag: 1 if age >= 60 else 0 (elevated baseline age risk)
    """

    def __init__(self, include_engineered: bool = True):
        self.include_engineered = include_engineered
        self.engineered_feature_names: List[str] = [
            "hr_max_ratio",
            "bp_chol_product",
            "exang_oldpeak_interaction",
            "age_risk_flag",
        ]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if not self.include_engineered:
            return X

        if isinstance(X, np.ndarray):
            # If passed as numpy array, convert to DataFrame using standard columns
            from src.config import settings
            X_df = pd.DataFrame(X, columns=settings.ALL_FEATURE_COLUMNS).copy()
        else:
            X_df = X.copy()

        # 1. Heart rate achieved relative to age-predicted maximum (220 - age)
        age_pred_max = np.clip(220.0 - X_df["age"], 40.0, 220.0)
        X_df["hr_max_ratio"] = X_df["thalach"] / age_pred_max

        # 2. Hemodynamic-lipid index: blood pressure * cholesterol
        X_df["bp_chol_product"] = (X_df["trestbps"] * X_df["chol"]) / 1000.0

        # 3. Exercise ischemia interaction: exercise angina * ST depression
        X_df["exang_oldpeak_interaction"] = X_df["exang"] * X_df["oldpeak"]

        # 4. Senior age flag (AHA cardiovascular risk inflection point at 60)
        X_df["age_risk_flag"] = (X_df["age"] >= 60).astype(float)

        return X_df

    def get_feature_names_out(self, input_features=None):
        if not self.include_engineered:
            return input_features
        if input_features is None:
            from src.config import settings
            input_features = list(settings.ALL_FEATURE_COLUMNS)
        return list(input_features) + self.engineered_feature_names
