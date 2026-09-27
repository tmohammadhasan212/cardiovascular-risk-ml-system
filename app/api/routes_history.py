"""FastAPI router for prediction history management, filtering, and CSV export."""

import csv
import io
import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.repository import PredictionRepository
from app.schemas.prediction import PredictionHistoryResponseSchema

router = APIRouter(prefix="/api/v1/history", tags=["History"])


@router.get(
    "",
    response_model=PredictionHistoryResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Retrieve prediction assessment history",
)
def get_prediction_history(
    skip: int = Query(0, ge=0, description="Records to skip for pagination"),
    limit: int = Query(50, ge=1, le=200, description="Max records to return"),
    risk_tier: Optional[str] = Query(
        None, description="Filter by risk tier (Low Risk, Moderate Risk, High Risk)"
    ),
    db: Session = Depends(get_db),
):
    records = PredictionRepository.get_history(
        db=db, skip=skip, limit=limit, risk_filter=risk_tier
    )
    total = PredictionRepository.get_total_count(db=db, risk_filter=risk_tier)

    items = [rec.to_dict() for rec in records]
    return {
        "total": total,
        "items": items,
        "skip": skip,
        "limit": limit,
    }


@router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
    summary="Get summary metrics of stored assessments",
)
def get_history_statistics(db: Session = Depends(get_db)):
    return PredictionRepository.get_history_summary_statistics(db)


@router.get(
    "/{prediction_id}",
    status_code=status.HTTP_200_OK,
    summary="Get single assessment record by ID",
)
def get_prediction_by_id(prediction_id: int, db: Session = Depends(get_db)):
    record = PredictionRepository.get_prediction_by_id(db, prediction_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction record with ID {prediction_id} not found.",
        )
    return record.to_dict()


@router.delete(
    "/{prediction_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete single assessment record by ID",
)
def delete_prediction_by_id(prediction_id: int, db: Session = Depends(get_db)):
    success = PredictionRepository.delete_prediction(db, prediction_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction record with ID {prediction_id} not found.",
        )
    return {"success": True, "deleted_id": prediction_id}


@router.get(
    "/export/csv",
    summary="Export all prediction records as CSV",
    response_class=StreamingResponse,
)
def export_predictions_csv(db: Session = Depends(get_db)):
    records = PredictionRepository.get_history(db=db, skip=0, limit=10000)

    output = io.StringIO()
    writer = csv.writer(output)

    # Write CSV header
    headers = [
        "id",
        "created_at",
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
        "prediction",
        "probability",
        "risk_tier",
        "model_version",
    ]
    writer.writerow(headers)

    for r in records:
        writer.writerow(
            [
                r.id,
                r.created_at.isoformat() if r.created_at else "",
                r.age,
                r.sex,
                r.cp,
                r.trestbps,
                r.chol,
                r.fbs,
                r.restecg,
                r.thalach,
                r.exang,
                r.oldpeak,
                r.slope,
                r.ca,
                r.thal,
                r.prediction,
                r.probability,
                r.risk_tier,
                r.model_version,
            ]
        )

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=cardiovascular_predictions.csv"},
    )
