"""Prediction service coordinating inference, explainability, and database persistence."""

from typing import Any, Dict, List
from sqlalchemy.orm import Session

from app.database.models import PredictionRecord
from app.database.repository import PredictionRepository
from app.schemas.prediction import PatientInputSchema
from src.models.predict import get_prediction_engine


class PredictionService:
    """Orchestrates patient risk inference, SHAP explanations, and persistence."""

    def __init__(self):
        self.engine = get_prediction_engine()

    def process_patient_prediction(
        self,
        db: Session,
        patient_input: PatientInputSchema,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """Run patient prediction, compute SHAP attributions, and persist record."""
        patient_dict = patient_input.to_features_dict()

        # Run inference and SHAP local attribution
        prediction_result = self.engine.predict_patient(patient_dict)

        record_id = None
        created_at_str = None

        if persist:
            record: PredictionRecord = PredictionRepository.create_prediction(
                db=db,
                patient_data=patient_dict,
                prediction_result=prediction_result,
            )
            record_id = record.id
            created_at_str = record.created_at.isoformat() if record.created_at else None

        prediction_result["id"] = record_id
        prediction_result["created_at"] = created_at_str

        return prediction_result

    def process_batch_predictions(
        self,
        db: Session,
        patients: List[PatientInputSchema],
        persist: bool = True,
    ) -> List[Dict[str, Any]]:
        """Run batch inference for multiple patient records."""
        results = []
        for patient in patients:
            res = self.process_patient_prediction(db=db, patient_input=patient, persist=persist)
            results.append(res)
        return results


prediction_service = PredictionService()


def get_prediction_service() -> PredictionService:
    """Retrieve singleton instance of PredictionService."""
    return prediction_service
