"""Pydantic schemas for patient inputs, prediction responses, and history queries."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class PatientInputSchema(BaseModel):
    """Clinical input parameters for patient cardiovascular assessment."""

    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in completed years",
        examples=[58],
    )
    sex: int = Field(
        ...,
        ge=0,
        le=1,
        description="Biological sex: 1 = male, 0 = female",
        examples=[1],
    )
    cp: int = Field(
        ...,
        ge=0,
        le=3,
        description="Chest pain type: 0: typical angina, 1: atypical angina, 2: non-anginal pain, 3: asymptomatic",
        examples=[2],
    )
    trestbps: float = Field(
        ...,
        ge=60.0,
        le=260.0,
        description="Resting systolic blood pressure (mm Hg)",
        examples=[135.0],
    )
    chol: float = Field(
        ...,
        ge=80.0,
        le=600.0,
        description="Serum cholesterol (mg/dl)",
        examples=[245.0],
    )
    fbs: int = Field(
        ...,
        ge=0,
        le=1,
        description="Fasting blood sugar > 120 mg/dl: 1 = true, 0 = false",
        examples=[0],
    )
    restecg: int = Field(
        ...,
        ge=0,
        le=2,
        description="Resting ECG results: 0: normal, 1: ST-T wave abnormality, 2: left ventricular hypertrophy",
        examples=[1],
    )
    thalach: float = Field(
        ...,
        ge=50.0,
        le=250.0,
        description="Maximum heart rate achieved during exercise (bpm)",
        examples=[152.0],
    )
    exang: int = Field(
        ...,
        ge=0,
        le=1,
        description="Exercise-induced angina: 1 = yes, 0 = no",
        examples=[0],
    )
    oldpeak: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="ST depression induced by exercise relative to rest (mm)",
        examples=[1.2],
    )
    slope: int = Field(
        ...,
        ge=0,
        le=2,
        description="Slope of peak exercise ST segment: 0: upsloping, 1: flat, 2: downsloping",
        examples=[1],
    )
    ca: int = Field(
        ...,
        ge=0,
        le=3,
        description="Number of major vessels (0-3) colored by flourosopy",
        examples=[0],
    )
    thal: int = Field(
        ...,
        ge=1,
        le=3,
        description="Thalassemia scan result: 1: normal, 2: fixed defect, 3: reversible defect",
        examples=[2],
    )

    def to_features_dict(self) -> Dict[str, Any]:
        """Convert input schema to dictionary for model prediction."""
        return self.model_dump()


class FeatureAttributionSchema(BaseModel):
    """Local explanation attribution for a specific feature from SHAP."""

    feature: str
    base_feature: str
    patient_value: Any
    attribution: float
    abs_attribution: float
    direction: str


class PredictionResponseSchema(BaseModel):
    """Standardized API response schema for patient prediction."""

    id: Optional[int] = None
    prediction: int = Field(
        ..., description="Binary classification (1 = high cardiovascular risk, 0 = low risk)"
    )
    probability: float = Field(
        ..., ge=0.0, le=1.0, description="Predicted risk probability"
    )
    risk_tier: str = Field(
        ..., description="Categorical risk stratification: Low Risk, Moderate Risk, High Risk"
    )
    model_version: str
    model_name: str
    feature_attributions: List[FeatureAttributionSchema] = Field(
        default_factory=list, description="Top SHAP feature attributions"
    )
    created_at: Optional[str] = None
    disclaimer: str = (
        "Academic machine-learning prototype for scientific evaluation. "
        "Not intended for clinical diagnosis or medical decision-making."
    )


class PredictionHistoryItemSchema(BaseModel):
    """Schema for individual persistent prediction record in history view."""

    id: int
    created_at: str
    patient_data: Dict[str, Any]
    prediction: int
    probability: float
    risk_tier: str
    model_version: str


class PredictionHistoryResponseSchema(BaseModel):
    """Paginated prediction history response."""

    total: int
    items: List[PredictionHistoryItemSchema]
    skip: int
    limit: int


class HealthResponseSchema(BaseModel):
    """Health check response schema."""

    status: str
    model_loaded: bool
    database_connected: bool
    version: str
