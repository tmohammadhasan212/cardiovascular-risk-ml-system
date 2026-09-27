"""Unit tests for dataset loading, validation, preprocessing, and feature engineering."""

import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from src.config import settings
from src.data.loading import get_train_test_split, load_raw_dataset, validate_dataset
from src.data.preprocessing import build_preprocessor, get_feature_names
from src.features.engineering import ClinicalFeatureEngineer


def test_load_raw_dataset():
    """Verify raw dataset loading, column mapping, and target binarization."""
    df = load_raw_dataset()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 303
    assert settings.TARGET_COLUMN in df.columns
    assert set(df[settings.TARGET_COLUMN].unique()).issubset({0, 1})
    for col in settings.ALL_FEATURE_COLUMNS:
        assert col in df.columns


def test_validate_dataset():
    """Verify validation summary metrics."""
    df = load_raw_dataset()
    summary = validate_dataset(df)
    assert summary["num_records"] == 303
    assert summary["num_features"] == 13
    assert summary["target_distribution"][0] == 164
    assert summary["target_distribution"][1] == 139
    assert summary["duplicate_rows"] == 0
    # Expected known missing values in Cleveland dataset
    assert summary["missing_values"]["ca"] == 4
    assert summary["missing_values"]["thal"] == 2


def test_train_test_split_no_leakage():
    """Verify train/test split has no overlapping samples and preserves stratification."""
    X_train, X_test, y_train, y_test = get_train_test_split()

    # Verify disjoint indices (strict leakage check)
    train_idx = set(X_train.index)
    test_idx = set(X_test.index)
    assert len(train_idx.intersection(test_idx)) == 0

    # Verify expected split ratio (80/20)
    assert len(X_train) == 242
    assert len(X_test) == 61

    # Verify stratified balance in both partitions
    train_prev = y_train.mean()
    test_prev = y_test.mean()
    assert abs(train_prev - test_prev) < 0.03


def test_preprocessor_pipeline_transformation():
    """Verify that preprocessing handles missing values, scales, and encodes correctly."""
    X_train, X_test, y_train, _ = get_train_test_split()
    preprocessor = build_preprocessor()

    # Fit ONLY on training data to prevent data leakage
    preprocessor.fit(X_train)

    X_train_proc = preprocessor.transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    # Check that no NaN values exist in transformed output
    assert not np.isnan(X_train_proc).any()
    assert not np.isnan(X_test_proc).any()

    # Feature names should be retrievable
    feat_names = get_feature_names(preprocessor)
    assert len(feat_names) == X_train_proc.shape[1]
    assert X_train_proc.shape[1] > len(settings.ALL_FEATURE_COLUMNS)


def test_clinical_feature_engineer():
    """Verify clinical feature engineering transformations."""
    engineer = ClinicalFeatureEngineer(include_engineered=True)
    sample_df = pd.DataFrame(
        [
            {
                "age": 60,
                "sex": 1,
                "cp": 2,
                "trestbps": 140,
                "chol": 240,
                "fbs": 0,
                "restecg": 1,
                "thalach": 160,
                "exang": 1,
                "oldpeak": 2.0,
                "slope": 1,
                "ca": 1,
                "thal": 2,
            }
        ]
    )

    transformed = engineer.transform(sample_df)
    assert "hr_max_ratio" in transformed.columns
    assert "bp_chol_product" in transformed.columns
    assert "exang_oldpeak_interaction" in transformed.columns
    assert "age_risk_flag" in transformed.columns

    # Check exact values:
    # 220 - 60 = 160 -> thalach / 160 = 1.0
    assert pytest.approx(transformed["hr_max_ratio"].iloc[0], 0.01) == 1.0
    # (140 * 240) / 1000 = 33.6
    assert pytest.approx(transformed["bp_chol_product"].iloc[0], 0.01) == 33.6
    # 1 * 2.0 = 2.0
    assert pytest.approx(transformed["exang_oldpeak_interaction"].iloc[0], 0.01) == 2.0
    # age 60 -> flag 1.0
    assert transformed["age_risk_flag"].iloc[0] == 1.0
