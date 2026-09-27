"""Repository layer abstracting database operations for predictions and model versions."""

import json
from typing import Any, Dict, List, Optional
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.database.models import ModelVersion, PredictionRecord


class PredictionRepository:
    """Handles CRUD queries for prediction history and analytics."""

    @staticmethod
    def create_prediction(
        db: Session,
        patient_data: Dict[str, Any],
        prediction_result: Dict[str, Any],
    ) -> PredictionRecord:
        """Persist a new patient prediction assessment."""
        top_features_json = None
        if "feature_attributions" in prediction_result:
            top_features_json = json.dumps(prediction_result["feature_attributions"])

        record = PredictionRecord(
            age=int(patient_data["age"]),
            sex=int(patient_data["sex"]),
            cp=int(patient_data["cp"]),
            trestbps=float(patient_data["trestbps"]),
            chol=float(patient_data["chol"]),
            fbs=int(patient_data["fbs"]),
            restecg=int(patient_data["restecg"]),
            thalach=float(patient_data["thalach"]),
            exang=int(patient_data["exang"]),
            oldpeak=float(patient_data["oldpeak"]),
            slope=int(patient_data["slope"]),
            ca=int(patient_data["ca"]),
            thal=int(patient_data["thal"]),
            prediction=int(prediction_result["prediction"]),
            probability=float(prediction_result["probability"]),
            risk_tier=str(prediction_result["risk_tier"]),
            top_features=top_features_json,
            model_version=str(prediction_result.get("model_version", "1.0.0")),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_history(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        risk_filter: Optional[str] = None,
    ) -> List[PredictionRecord]:
        """Query paginated prediction records with optional risk tier filtering."""
        query = db.query(PredictionRecord)
        if risk_filter:
            query = query.filter(PredictionRecord.risk_tier == risk_filter)
        return (
            query.order_by(desc(PredictionRecord.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_total_count(db: Session, risk_filter: Optional[str] = None) -> int:
        """Count total predictions matching filter criteria."""
        query = db.query(func.count(PredictionRecord.id))
        if risk_filter:
            query = query.filter(PredictionRecord.risk_tier == risk_filter)
        return query.scalar() or 0

    @staticmethod
    def get_prediction_by_id(db: Session, prediction_id: int) -> Optional[PredictionRecord]:
        """Fetch a specific prediction assessment by primary key."""
        return (
            db.query(PredictionRecord)
            .filter(PredictionRecord.id == prediction_id)
            .first()
        )

    @staticmethod
    def delete_prediction(db: Session, prediction_id: int) -> bool:
        """Delete an assessment record by primary key."""
        record = (
            db.query(PredictionRecord)
            .filter(PredictionRecord.id == prediction_id)
            .first()
        )
        if not record:
            return False
        db.delete(record)
        db.commit()
        return True

    @staticmethod
    def get_history_summary_statistics(db: Session) -> Dict[str, Any]:
        """Compute aggregate statistics on persistent prediction history."""
        total = db.query(func.count(PredictionRecord.id)).scalar() or 0
        if total == 0:
            return {
                "total_assessments": 0,
                "low_risk_count": 0,
                "moderate_risk_count": 0,
                "high_risk_count": 0,
                "average_predicted_risk": 0.0,
            }

        low_count = (
            db.query(func.count(PredictionRecord.id))
            .filter(PredictionRecord.risk_tier == "Low Risk")
            .scalar()
            or 0
        )
        mod_count = (
            db.query(func.count(PredictionRecord.id))
            .filter(PredictionRecord.risk_tier == "Moderate Risk")
            .scalar()
            or 0
        )
        high_count = (
            db.query(func.count(PredictionRecord.id))
            .filter(PredictionRecord.risk_tier == "High Risk")
            .scalar()
            or 0
        )
        avg_prob = (
            db.query(func.avg(PredictionRecord.probability)).scalar() or 0.0
        )

        return {
            "total_assessments": total,
            "low_risk_count": low_count,
            "moderate_risk_count": mod_count,
            "high_risk_count": high_count,
            "average_predicted_risk": round(float(avg_prob), 4),
        }
