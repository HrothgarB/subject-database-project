from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_permission
from app.core.security import Permission
from app.db.session import get_db
from app.models.entities import Encounter, Subject, User
from app.schemas.subject import EncounterCreate, EncounterOut, SubjectCreate, SubjectOut, SubjectUpdate
from app.services.crypto import encrypt_ssn

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.post("", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
def create_subject(
    payload: SubjectCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_permission(Permission.SUBJECT_WRITE))],
):
    now = datetime.now(UTC)
    subject = Subject(
        first_name=payload.first_name,
        middle_name=payload.middle_name,
        last_name=payload.last_name,
        dob=payload.dob,
        alias=payload.alias,
        phone=payload.phone,
        address=payload.address,
        notes=payload.notes,
        case_number=payload.case_number,
        intel_number=payload.intel_number,
        restricted_ssn_ciphertext=encrypt_ssn(payload.restricted_ssn) if payload.restricted_ssn else None,
        created_by_id=user.id,
        created_at=now,
        updated_at=now,
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.get("", response_model=list[SubjectOut])
def search_subjects(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_permission(Permission.SUBJECT_READ))],
    q: str | None = Query(default=None),
    case_number: str | None = Query(default=None),
    intel_number: str | None = Query(default=None),
):
    stmt = select(Subject)
    if q:
        like_q = f"%{q}%"
        stmt = stmt.where(
            or_(
                Subject.first_name.ilike(like_q),
                Subject.last_name.ilike(like_q),
                Subject.alias.ilike(like_q),
            )
        )
    if case_number:
        stmt = stmt.where(Subject.case_number == case_number)
    if intel_number:
        stmt = stmt.where(Subject.intel_number == intel_number)
    return list(db.scalars(stmt.order_by(Subject.updated_at.desc())).all())


@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(
    subject_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_permission(Permission.SUBJECT_READ))],
):
    subject = db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    return subject


@router.patch("/{subject_id}", response_model=SubjectOut)
def update_subject(
    subject_id: int,
    payload: SubjectUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_permission(Permission.SUBJECT_WRITE))],
):
    subject = db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "restricted_ssn":
            subject.restricted_ssn_ciphertext = encrypt_ssn(value) if value else None
        else:
            setattr(subject, key, value)
    subject.updated_at = datetime.now(UTC)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.post("/{subject_id}/encounters", response_model=EncounterOut, status_code=status.HTTP_201_CREATED)
def create_encounter(
    subject_id: int,
    payload: EncounterCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_permission(Permission.ENCOUNTER_WRITE))],
):
    if not db.get(Subject, subject_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    encounter = Encounter(
        subject_id=subject_id,
        officer_id=user.id,
        location=payload.location,
        summary=payload.summary,
        encountered_at=payload.encountered_at,
    )
    db.add(encounter)
    db.commit()
    db.refresh(encounter)
    return encounter


@router.get("/{subject_id}/encounters", response_model=list[EncounterOut])
def list_encounters(
    subject_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_permission(Permission.SUBJECT_READ))],
):
    return list(db.scalars(select(Encounter).where(Encounter.subject_id == subject_id).order_by(Encounter.encountered_at.desc())).all())


@router.get("/{subject_id}/export")
def export_subject(
    subject_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_permission(Permission.SUBJECT_EXPORT))],
):
    subject = db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    # NOTE: Kept simple for MVP; can evolve into asynchronous report generation.
    return {"subject_id": subject.id, "full_name": f"{subject.first_name} {subject.last_name}", "case_number": subject.case_number}


@router.get("/me/profile")
def me(user: Annotated[User, Depends(get_current_user)]):
    return {"id": user.id, "email": user.email, "role": user.role}
