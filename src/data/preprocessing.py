"""Data preprocessing module using scikit-learn ColumnTransformer pipelines.

Guarantees that imputation and scaling parameters are learned strictly from training data.
"""

from typing import List, Optional
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import settings


def build_preprocessor(
    numerical_features: Optional[List[str]] = None,
    categorical_features: Optional[List[str]] = None,
    scale_numeric: bool = True,
) -> ColumnTransformer:
    """Build a ColumnTransformer pipeline for tabular cardiovascular data.
    
    Parameters
    ----------
    numerical_features : list of str, optional
        Column names to treat as numerical (median imputed, standard scaled).
    categorical_features : list of str, optional
        Column names to treat as categorical (mode imputed, one-hot encoded).
    scale_numeric : bool, default=True
        Whether to apply StandardScaler to numerical features.
        
    Returns
    -------
    ColumnTransformer
        Unfitted preprocessor pipeline.
    """
    num_cols = numerical_features or settings.NUMERICAL_FEATURES
    cat_cols = categorical_features or settings.CATEGORICAL_FEATURES

    # Numeric sub-pipeline
    num_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        num_steps.append(("scaler", StandardScaler()))
    numeric_transformer = Pipeline(steps=num_steps)

    # Categorical sub-pipeline
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    return preprocessor


def get_feature_names(preprocessor: ColumnTransformer) -> List[str]:
    """Retrieve output feature names from a fitted ColumnTransformer."""
    try:
        return list(preprocessor.get_feature_names_out())
    except Exception:
        # Fallback if get_feature_names_out fails
        feature_names = []
        for name, trans, cols in preprocessor.transformers_:
            if name == "remainder" and trans == "drop":
                continue
            if hasattr(trans, "get_feature_names_out"):
                feature_names.extend(trans.get_feature_names_out(cols))
            else:
                feature_names.extend(cols)
        return feature_names
