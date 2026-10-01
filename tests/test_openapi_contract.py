"""Guards against drift between the hand-written openapi.yaml (checked by the
Foundation governance gate) and the routes FastAPI actually serves."""
from pathlib import Path

import yaml

from src.main import app

_METHODS = {"get", "post", "put", "patch", "delete"}


def _operations(paths: dict) -> set:
    return {(m, p) for p, ops in paths.items() for m in ops if m in _METHODS}


def test_openapi_yaml_matches_served_routes():
    spec = yaml.safe_load((Path(__file__).parent.parent / "openapi.yaml").read_text(encoding="utf-8"))
    assert _operations(spec["paths"]) == _operations(app.openapi()["paths"])
