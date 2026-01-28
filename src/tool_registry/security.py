import hmac
import hashlib
import base64
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.tool_registry.config import load_service_config

service_config = load_service_config()
security = HTTPBearer(auto_error=False)


def _generate_admin_token(secret: str) -> str:
    digest = hmac.new(secret.encode(), b"admin-access", hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode()


ADMIN_TOKEN = _generate_admin_token(service_config.admin_auth_key)


def admin_bypass(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> bool:
    if credentials is None:
        return False

    return secrets.compare_digest(
        credentials.credentials,
        ADMIN_TOKEN,
    )


def normal_auth() -> bool:
    return False


def require_auth_or_admin(
    is_admin: bool = Depends(admin_bypass),
    user=Depends(normal_auth),
):
    if is_admin:
        return {"role": "admin"}

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
