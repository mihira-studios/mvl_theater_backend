import os
import requests
import logging
log = logging.getLogger(__name__)

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

KC_BASE = os.getenv("KC_BASE", "http://10.100.1.30:8080")
KC_ISSUER = os.getenv("KC_BASE", "http://10.100.1.30:8080")
REALM = os.getenv("KC_RELAM","MIHIRA-REALM")
ALGORITHMS = ["RS256"]

bearer_scheme = HTTPBearer()
_jwks_cache = None

def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        jwks_url = f"{KC_BASE}/realms/{REALM}/protocol/openid-connect/certs"
        _jwks_cache = requests.get(jwks_url, timeout=5).json()
    return _jwks_cache

def verify_keycloak_token(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),):
    token = creds.credentials
    jwks = get_jwks()

    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]
        key = next(k for k in jwks["keys"] if k["kid"] == kid)

        payload = jwt.decode(
            token,
            key,
            algorithms=ALGORITHMS,
            issuer=f"{KC_ISSUER}/realms/{REALM}",
            options={"verify_aud": False},  
        )

        log.debug("KC token ok for sub=%s", payload.get("sub"))
        return payload

    except (StopIteration, JWTError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )