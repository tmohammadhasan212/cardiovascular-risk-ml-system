"""Dataset loading, validation, and train/test splitting module.

Ensures complete reproducibility and strict prevention of data leakage.
"""

from pathlib import Path
from typing import Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import settings


def load_raw_dataset(csv_path: Optional[Path] = None) -> pd.DataFrame:
    """Load the raw UCI Heart Disease dataset.
    
    Converts 'num' or 'target' to binary {0, 1}, cleans column names,
    replaces missing indicator strings ('?', 'NA') with np.nan, and enforces schemas.
    """
    path = csv_path or settings.RAW_DATA_PATH
    if not Path(path).exists():
        raise FileNotFoundError(f"Dataset file not found at: {path}")

    df = pd.read_csv(path, na_values=["?", "NA", "null", ""])

    # Rename target column if represented as 'num' in UCI Cleveland raw data
    if "num" in df.columns and "target" not in df.columns:
        df = df.rename(columns={"num": "target"})

    # Validate target presence
    if "target" not in df.columns:
        raise ValueError("Missing 'target' or 'num' column in dataset.")

    # Convert multiclass stages (0=absence, 1-4=presence) to binary classification {0, 1}
    df["target"] = (df["target"] > 0).astype(int)

    # Validate required features
    missing_cols = [c for c in settings.ALL_FEATURE_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset missing required feature columns: {missing_cols}")

    # Enforce numeric types
    for col in settings.ALL_FEATURE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def validate_dataset(df: pd.DataFrame) -> dict:
    """Perform structural data quality validation and return summary statistics."""
    summary = {
        "num_records": len(df),
        "num_features": len(settings.ALL_FEATURE_COLUMNS),
        "target_distribution": df[settings.TARGET_COLUMN].value_counts().to_dict(),
        "target_percentages": (
            df[settings.TARGET_COLUMN].value_counts(normalize=True) * 100
        ).round(2).to_dict(),
        "missing_values": df[settings.ALL_FEATURE_COLUMNS].isnull().sum().to_dict(),
        "total_missing_cells": int(df[settings.ALL_FEATURE_COLUMNS].isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated(subset=settings.ALL_FEATURE_COLUMNS).sum()),
    }
    return summary


def get_train_test_split(
    df: Optional[pd.DataFrame] = None,
    test_size: Optional[float] = None,
    random_state: Optional[int] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split dataset into stratified train and test partitions.
    
    Splitting occurs BEFORE any preprocessing or transformation to prevent data leakage.
    """
    if df is None:
        df = load_raw_dataset()

    test_size = test_size if test_size is not None else settings.TEST_SIZE
    random_state = random_state if random_state is not None else settings.RANDOM_STATE

    X = df[settings.ALL_FEATURE_COLUMNS].copy()
    y = df[settings.TARGET_COLUMN].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    return X_train, X_test, y_train, y_test
