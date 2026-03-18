from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.middleware.audit import AuditLoggingMiddleware
from app.middleware.auth_context import AuthContextMiddleware

app = FastAPI(title=settings.app_name)

app.add_middleware(AuthContextMiddleware)
app.add_middleware(AuditLoggingMiddleware)
app.include_router(api_router)


@app.get("/healthz")
def healthcheck():
    return {"status": "ok"}
