from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Role(StrEnum):
    ADMIN = "admin"
    ANALYST = "analyst"
    OFFICER = "officer"


class Permission(StrEnum):
    SUBJECT_READ = "subject:read"
    SUBJECT_WRITE = "subject:write"
    SUBJECT_EXPORT = "subject:export"
    ENCOUNTER_WRITE = "encounter:write"
    USER_MANAGE = "user:manage"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.ADMIN: {
        Permission.SUBJECT_READ,
        Permission.SUBJECT_WRITE,
        Permission.SUBJECT_EXPORT,
        Permission.ENCOUNTER_WRITE,
        Permission.USER_MANAGE,
    },
    Role.ANALYST: {
        Permission.SUBJECT_READ,
        Permission.SUBJECT_WRITE,
        Permission.SUBJECT_EXPORT,
        Permission.ENCOUNTER_WRITE,
    },
    Role.OFFICER: {
        Permission.SUBJECT_READ,
        Permission.SUBJECT_WRITE,
        Permission.ENCOUNTER_WRITE,
    },
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(subject: str, token_type: str, minutes: int, extras: dict[str, Any] | None = None) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    }
    if extras:
        payload.update(extras)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
