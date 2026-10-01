"""Thin binding over cloudforge_auth_core. This Studio is a resource server
only: it verifies tokens from the Identity Service and never issues its own."""
from cloudforge_auth_core import Principal, build_auth_dependencies
from cloudforge_auth_core.jwks import JWKSCache

from src.auth.config import build_auth_config

_config = build_auth_config()
_jwks_cache = JWKSCache(_config)
get_current_user, require_scope = build_auth_dependencies(_config, jwks_cache=_jwks_cache)

__all__ = ["get_current_user", "require_scope", "Principal", "_jwks_cache"]
