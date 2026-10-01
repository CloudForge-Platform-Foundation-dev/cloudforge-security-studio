import pytest
from fastapi.testclient import TestClient

from src.api.routes import get_store
from src.auth import dependencies as auth_deps
from src.main import app
from src.store import EventStore
from tests.helpers import PUBLIC_KEY, FakeSigningKey


@pytest.fixture(autouse=True)
def _jwks_patch(monkeypatch):
    monkeypatch.setattr(
        auth_deps._jwks_cache, "get_signing_key", lambda token: FakeSigningKey(PUBLIC_KEY)
    )


@pytest.fixture
def store():
    s = EventStore()
    app.dependency_overrides[get_store] = lambda: s
    yield s
    app.dependency_overrides.clear()


@pytest.fixture
def client(store):
    return TestClient(app)
