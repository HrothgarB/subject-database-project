import base64
from hashlib import sha256

from app.core.config import settings


# NOTE: This placeholder demonstrates where field-level encryption plugs in.
# Replace with envelope encryption using KMS/HSM in production.
def encrypt_ssn(raw_value: str) -> str:
    digest = sha256(f"{settings.jwt_secret}:{raw_value}".encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8")
