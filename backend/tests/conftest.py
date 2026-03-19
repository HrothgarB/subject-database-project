import os
from datetime import UTC, date, datetime
from pathlib import Path

from fastapi.testclient import TestClient

TEST_DB_PATH = Path(__file__).with_name("test.db")
os.environ.setdefault("SUBJECT_DATABASE_URL", f"sqlite:///{TEST_DB_PATH.as_posix()}")
os.environ.setdefault("SUBJECT_JWT_SECRET", "test-secret")
os.environ.setdefault("SUBJECT_SSN_ENCRYPTION_SECRET", "test-secret")

from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine
from app.main import app
from app.models.entities import Subject, User


def _seed_user(
    email: str = "admin@agency.local",
    password: str = "Password!123",
    role: str = "admin",
) -> User:
    db = SessionLocal()
    try:
        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            full_name="Admin User",
            role=role,
            is_active=True,
            created_at=datetime.now(UTC),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def _seed_subject(created_by_id: int) -> Subject:
    db = SessionLocal()
    try:
        subject = Subject(
            first_name="Jordan",
            middle_name="A",
            last_name="Mills",
            dob=date(1990, 5, 1),
            alias="JM",
            phone="555-0101",
            address="100 Main St",
            notes="Seed profile for integration testing.",
            case_number="CASE-1001",
            intel_number="INTEL-1001",
            restricted_ssn_ciphertext=None,
            created_by_id=created_by_id,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        db.add(subject)
        db.commit()
        db.refresh(subject)
        return subject
    finally:
        db.close()


def pytest_sessionstart(session):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def pytest_sessionfinish(session, exitstatus):
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


import pytest


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def admin_user():
    return _seed_user()


@pytest.fixture()
def admin_token(client, admin_user):
    response = client.post(
        "/api/auth/login",
        json={"email": admin_user.email, "password": "Password!123"},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture()
def subject(admin_user):
    return _seed_subject(admin_user.id)
