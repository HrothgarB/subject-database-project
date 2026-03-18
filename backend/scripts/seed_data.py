from datetime import UTC, date, datetime

from sqlalchemy import delete

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.entities import Subject, User
from app.services.crypto import encrypt_ssn


def run() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(Subject))
        db.execute(delete(User))

        admin = User(
            email="admin@agency.local",
            hashed_password=get_password_hash("Password!123"),
            full_name="Admin User",
            role="admin",
            is_active=True,
            created_at=datetime.now(UTC),
        )
        db.add(admin)
        db.flush()

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
            restricted_ssn_ciphertext=encrypt_ssn("111-22-3333"),
            created_by_id=admin.id,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        db.add(subject)
        db.commit()
        print("Seed data inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
