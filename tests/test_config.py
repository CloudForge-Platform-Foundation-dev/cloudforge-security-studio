from src.auth.config import AuthSettings, build_auth_config


def test_env_vars_are_honored(monkeypatch):
    monkeypatch.setenv("AUTH_JWT_ISSUER", "https://issuer.test")
    monkeypatch.setenv("AUTH_JWT_AUDIENCE", "aud.test")
    monkeypatch.setenv("AUTH_JWKS_URL", "https://issuer.test/jwks.json")
    cfg = build_auth_config(AuthSettings())
    assert (cfg.issuer, cfg.audience, cfg.jwks_url) == (
        "https://issuer.test", "aud.test", "https://issuer.test/jwks.json",
    )
    assert tuple(cfg.algorithms) == ("RS256",)
