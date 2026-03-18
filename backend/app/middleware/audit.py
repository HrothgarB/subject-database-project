from datetime import UTC, datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import SessionLocal
from app.models.entities import AuditLog

AUDITED_PREFIXES = ("/api/subjects", "/api/photos")


def classify_action(method: str) -> str:
    if method == "GET":
        return "read"
    if method == "POST":
        return "create"
    if method in {"PUT", "PATCH"}:
        return "update"
    return method.lower()


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if request.url.path.startswith(AUDITED_PREFIXES):
            db = SessionLocal()
            try:
                log = AuditLog(
                    actor_user_id=getattr(request.state, "user_id", None),
                    action=classify_action(request.method),
                    resource_type=request.url.path.split("/")[2] if len(request.url.path.split("/")) > 2 else "unknown",
                    resource_id=None,
                    method=request.method,
                    path=request.url.path,
                    ip_address=request.client.host if request.client else None,
                    meta={"status_code": response.status_code},
                    created_at=datetime.now(UTC),
                )
                db.add(log)
                db.commit()
            finally:
                db.close()
        return response
