from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.security import Permission
from app.db.session import get_db
from app.models.entities import Subject, SubjectPhoto, User
from app.services.object_storage import object_storage_service

router = APIRouter(prefix="/photos", tags=["photos"])


@router.post("/subjects/{subject_id}", status_code=status.HTTP_201_CREATED)
def upload_subject_photo(
    subject_id: int,
    file: UploadFile = File(...),
    db: Annotated[Session, Depends(get_db)] = None,
    _: Annotated[User, Depends(require_permission(Permission.SUBJECT_WRITE))] = None,
):
    if not db.get(Subject, subject_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    # MVP: ingest metadata only; replace with streaming upload to encrypted object storage.
    object_key = object_storage_service.create_object_key(subject_id=subject_id, filename=file.filename or "capture.jpg")
    photo = SubjectPhoto(
        subject_id=subject_id,
        object_key=object_key,
        content_type=file.content_type or "image/jpeg",
        captured_at=datetime.now(UTC),
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return {"id": photo.id, "object_key": photo.object_key}
