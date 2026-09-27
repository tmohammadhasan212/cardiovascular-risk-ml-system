"""Configuration settings for the cardiovascular risk machine learning system."""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_PATH: Path = DATA_DIR / "raw" / "heart_disease.csv"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    MODELS_DIR: Path = BASE_DIR / "models"
    MODEL_PATH: Path = MODELS_DIR / "best_model.joblib"
    METADATA_PATH: Path = MODELS_DIR / "model_metadata.json"

    # Application settings
    APP_NAME: str = "Cardiovascular Risk ML System"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000

    # Persistence settings
    DATABASE_URL: str = "sqlite:///./cardio_risk.db"

    # Reproducibility & ML parameters
    RANDOM_STATE: int = 42
    TEST_SIZE: float = 0.20
    CV_FOLDS: int = 5

    # Features schema definition
    TARGET_COLUMN: str = "target"

    NUMERICAL_FEATURES: List[str] = [
        "age",
        "trestbps",
        "chol",
        "thalach",
        "oldpeak",
        "ca",
    ]

    CATEGORICAL_FEATURES: List[str] = [
        "sex",
        "cp",
        "fbs",
        "restecg",
        "exang",
        "slope",
        "thal",
    ]

    ALL_FEATURE_COLUMNS: List[str] = [
        "age",
        "sex",
        "cp",
        "trestbps",
        "chol",
        "fbs",
        "restecg",
        "thalach",
        "exang",
        "oldpeak",
        "slope",
        "ca",
        "thal",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
