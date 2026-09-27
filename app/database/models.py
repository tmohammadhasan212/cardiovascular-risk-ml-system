"""SQLAlchemy ORM models for prediction persistence and model versioning."""

from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from app.database.connection import Base


class PredictionRecord(Base):
    """Stores individual patient prediction evaluations and clinical input parameters."""

    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    # 13 Clinical Patient Attributes
    age = Column(Integer, nullable=False)
    sex = Column(Integer, nullable=False)
    cp = Column(Integer, nullable=False)
    trestbps = Column(Float, nullable=False)
    chol = Column(Float, nullable=False)
    fbs = Column(Integer, nullable=False)
    restecg = Column(Integer, nullable=False)
    thalach = Column(Float, nullable=False)
    exang = Column(Integer, nullable=False)
    oldpeak = Column(Float, nullable=False)
    slope = Column(Integer, nullable=False)
    ca = Column(Integer, nullable=False)
    thal = Column(Integer, nullable=False)

    # Prediction outputs
    prediction = Column(Integer, nullable=False)
    probability = Column(Float, nullable=False)
    risk_tier = Column(String(50), nullable=False, index=True)
    top_features = Column(Text, nullable=True)  # JSON-encoded top SHAP attributions
    model_version = Column(String(50), nullable=False)

    def to_dict(self):
        """Serialize record to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "patient_data": {
                "age": self.age,
                "sex": self.sex,
                "cp": self.cp,
                "trestbps": self.trestbps,
                "chol": self.chol,
                "fbs": self.fbs,
                "restecg": self.restecg,
                "thalach": self.thalach,
                "exang": self.exang,
                "oldpeak": self.oldpeak,
                "slope": self.slope,
                "ca": self.ca,
                "thal": self.thal,
            },
            "prediction": self.prediction,
            "probability": self.probability,
            "risk_tier": self.risk_tier,
            "model_version": self.model_version,
        }


class ModelVersion(Base):
    """Tracks deployed model metadata, versions, and validation metrics."""

    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    version = Column(String(50), unique=True, index=True, nullable=False)
    model_name = Column(String(100), nullable=False)
    training_date = Column(DateTime(timezone=True), nullable=False)
    dataset_version = Column(String(50), default="UCI Cleveland 14-attr")
    metrics = Column(Text, nullable=True)  # JSON-encoded test & CV metrics
    is_active = Column(Boolean, default=True)
