"""Pytest configuration and shared test database fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.connection import Base, get_db
from app.database.models import ModelVersion, PredictionRecord  # noqa: F401
from app.main import app

# Single shared in-memory test database with StaticPool
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Set the global override once
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clean_db():
    """Clear database records before each test to maintain state isolation."""
    db = TestingSessionLocal()
    db.query(PredictionRecord).delete()
    db.query(ModelVersion).delete()
    db.commit()
    db.close()
    yield


@pytest.fixture
def client():
    """Test client fixture configured with test database."""
    return TestClient(app)
