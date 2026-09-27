"""FastAPI router for patient risk prediction and batch inference."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.prediction import (
    PatientInputSchema,
    PredictionResponseSchema,
)
from app.services.prediction_service import get_prediction_service, PredictionService

router = APIRouter(prefix="/api/v1/predict", tags=["Prediction"])


@router.post(
    "",
    response_model=PredictionResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Predict cardiovascular risk for a patient",
    description=(
        "Accepts 13 clinical patient parameters, runs the optimized machine-learning "
        "pipeline to calculate disease probability and risk tier, generates local SHAP "
        "feature attributions, and persists the assessment record."
    ),
)
def predict_patient(
    patient_input: PatientInputSchema,
    db: Session = Depends(get_db),
    service: PredictionService = Depends(get_prediction_service),
):
    try:
        result = service.process_patient_prediction(
            db=db, patient_input=patient_input, persist=True
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}",
        )


@router.post(
    "/batch",
    response_model=List[PredictionResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Batch cardiovascular risk prediction",
    description="Evaluate multiple patient records concurrently.",
)
def predict_batch(
    patients: List[PatientInputSchema],
    persist: bool = True,
    db: Session = Depends(get_db),
    service: PredictionService = Depends(get_prediction_service),
):
    try:
        results = service.process_batch_predictions(
            db=db, patients=patients, persist=persist
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}",
        )
