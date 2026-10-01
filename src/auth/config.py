"""Auth settings — supplies environment-specific values to the shared AuthConfig.
Do NOT re-implement JWT verification here (Identity Contract v1)."""
from pydantic_settings import BaseSettings, SettingsConfigDict

from cloudforge_auth_core import AuthConfig


class AuthSettings(BaseSettings):
    # env: AUTH_JWT_ISSUER, AUTH_JWT_AUDIENCE, AUTH_JWKS_URL, AUTH_JWKS_CACHE_TTL_SECONDS
    model_config = SettingsConfigDict(env_prefix="AUTH_")

    jwt_issuer: str = "https://identity.cloudforge.internal"
    # Contract v1 §2: audience is platform-wide, not per-Studio.
    jwt_audience: str = "cloudforge-platform"
    jwks_url: str = "https://identity.cloudforge.internal/.well-known/jwks.json"
    jwks_cache_ttl_seconds: int = 3600


auth_settings = AuthSettings()


def build_auth_config(settings: AuthSettings | None = None) -> AuthConfig:
    s = settings or auth_settings
    return AuthConfig(
        issuer=s.jwt_issuer,
        audience=s.jwt_audience,
        jwks_url=s.jwks_url,
        jwks_cache_ttl_seconds=s.jwks_cache_ttl_seconds,
    )
