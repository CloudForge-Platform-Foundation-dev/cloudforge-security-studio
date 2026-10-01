import time
from uuid import uuid4

import jwt as pyjwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from src.auth.config import auth_settings

PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PUBLIC_KEY = PRIVATE_KEY.public_key()
_PRIVATE_PEM = PRIVATE_KEY.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)


class FakeSigningKey:
    def __init__(self, key):
        self.key = key


def make_token(scope="security:read", **overrides) -> str:
    now = int(time.time())
    claims = {
        "sub": "test-user",
        "iss": auth_settings.jwt_issuer,
        "aud": auth_settings.jwt_audience,
        "iat": now,
        "exp": now + 3600,
        "scope": scope,
    }
    claims.update(overrides)
    return pyjwt.encode(claims, _PRIVATE_PEM, algorithm="RS256")


def auth(scope: str, **overrides) -> dict:
    return {"Authorization": f"Bearer {make_token(scope, **overrides)}"}


def make_event(event_type="Finding.Created", payload=None, **overrides) -> dict:
    event = {
        "eventId": str(uuid4()),
        "eventType": event_type,
        "source": "ingest-studio",
        "timestamp": "2026-09-30T10:00:00Z",
        "payload": payload
        if payload is not None
        else {"severity": "HIGH", "title": "Hardcoded password", "resource": "src/app.py"},
    }
    event.update(overrides)
    return event
