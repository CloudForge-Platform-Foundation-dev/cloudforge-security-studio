"""HTTP-level auth tests — Identity Contract v1 semantics (401 / 403 / 503)."""
import time

import pytest

from cloudforge_auth_core import JWKSUnavailableError
from src.auth import dependencies as auth_deps
from src.auth.config import auth_settings
from tests.helpers import auth, make_event, make_token

READ, WRITE = "security:read", "security:write"


def test_health_needs_no_token(client):
    assert client.get("/health").status_code == 200


def test_findings_without_token_is_401(client):
    assert client.get("/findings").status_code == 401


def test_events_without_token_is_401(client):
    assert client.post("/events", json=make_event()).status_code == 401


def test_garbage_token_is_401(client):
    resp = client.get("/findings", headers={"Authorization": "Bearer not-a-real-jwt"})
    assert resp.status_code == 401


def test_read_token_cannot_write_is_403(client):
    assert client.post("/events", json=make_event(), headers=auth(READ)).status_code == 403


def test_write_token_cannot_read_is_403(client):
    assert client.get("/findings", headers=auth(WRITE)).status_code == 403


def test_correct_scope_succeeds(client):
    assert client.get("/findings", headers=auth(READ)).status_code == 200


def test_deprecated_scopes_list_is_401(client):
    token = make_token(scope="ignored", scopes=[READ])
    resp = client.get("/findings", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401


def test_expired_token_is_401(client):
    now = int(time.time())
    headers = auth(READ, iat=now - 7200, exp=now - 3600)
    assert client.get("/findings", headers=headers).status_code == 401


@pytest.mark.parametrize("claim,value", [("aud", "someone-else"), ("iss", "https://evil.example")])
def test_wrong_audience_or_issuer_is_401(client, claim, value):
    assert client.get("/findings", headers=auth(READ, **{claim: value})).status_code == 401


def test_jwks_unavailable_is_503(client, monkeypatch):
    def _down(token):
        raise JWKSUnavailableError("identity service down")

    monkeypatch.setattr(auth_deps._jwks_cache, "get_signing_key", _down)
    assert client.get("/findings", headers=auth(READ)).status_code == 503
