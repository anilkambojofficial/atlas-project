"""Identity cryptography tests (ES-007 §5 — deterministic, no network)."""

from __future__ import annotations

import pytest

from apps.identity import security
from apps.identity.domain import validate_organization_slug, validate_password_policy
from shared.config import Settings
from shared.exceptions import AuthenticationError, ValidationError


def _settings(**overrides) -> Settings:
    return Settings(**overrides)


class TestPasswordHashing:
    def test_hash_and_verify_roundtrip(self) -> None:
        digest = security.hash_password("Str0ng-Password-Example")
        assert digest.startswith("$argon2id$")
        assert security.verify_password("Str0ng-Password-Example", digest)

    def test_wrong_password_rejected(self) -> None:
        digest = security.hash_password("Str0ng-Password-Example")
        assert not security.verify_password("Wrong-Password-1", digest)

    def test_malformed_hash_rejected(self) -> None:
        assert not security.verify_password("anything", "not-a-hash")

    def test_token_digest_is_stable_sha256(self) -> None:
        assert security.token_digest("abc") == security.token_digest("abc")
        assert len(security.token_digest("abc")) == 64


class TestPasswordPolicy:
    def test_policy_accepts_strong_password(self) -> None:
        validate_password_policy("Adequate-Passw0rd", min_length=12)

    @pytest.mark.parametrize(
        "candidate", ["short-A1", "alllowercase1234", "ALLUPPERCASE1234", "NoDigitsHerePassword"]
    )
    def test_policy_rejects_weak_passwords(self, candidate: str) -> None:
        with pytest.raises(ValidationError):
            validate_password_policy(candidate, min_length=12)


class TestSlugPolicy:
    def test_valid_slug(self) -> None:
        validate_organization_slug("acme-corp-01")

    @pytest.mark.parametrize("slug", ["", "-acme", "acme-", "Acme", "a b", "a_b"])
    def test_invalid_slugs(self, slug: str) -> None:
        with pytest.raises(ValidationError):
            validate_organization_slug(slug)


class TestJwtTokens:
    def _issue(self, service: security.JwtTokenService) -> str:
        return service.issue_access_token(
            user_id="0198f5a0-0000-7000-8000-00000000000a",
            organization_id="0198f5a0-0000-7000-8000-00000000000b",
            roles=("owner",),
            permissions=("identity.user.read",),
            display_name="Test User",
            session_id="0198f5a0-0000-7000-8000-00000000000c",
        )

    @pytest.mark.asyncio
    async def test_issue_verify_roundtrip(self) -> None:
        service = security.JwtTokenService(_settings())
        principal = await service.verify(self._issue(service))
        assert principal.subject_id == "0198f5a0-0000-7000-8000-00000000000a"
        assert principal.organization_id == "0198f5a0-0000-7000-8000-00000000000b"
        assert principal.roles == ("owner",)
        assert "identity.user.read" in principal.permissions

    @pytest.mark.asyncio
    async def test_tampered_token_rejected(self) -> None:
        service = security.JwtTokenService(_settings())
        token = self._issue(service)
        with pytest.raises(AuthenticationError):
            await service.verify(token[:-4] + "AAAA")

    @pytest.mark.asyncio
    async def test_wrong_secret_rejected(self) -> None:
        token = self._issue(security.JwtTokenService(_settings()))
        other = security.JwtTokenService(_settings(auth_jwt_secret="another-secret-of-sufficient-length-123456"))
        with pytest.raises(AuthenticationError):
            await other.verify(token)

    @pytest.mark.asyncio
    async def test_expired_token_rejected(self) -> None:
        service = security.JwtTokenService(
            _settings(auth_access_token_ttl_seconds=60)
        )
        import jwt as pyjwt
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        expired = pyjwt.encode(
            {
                "iss": "atlas-identity",
                "sub": "u",
                "iat": now - timedelta(hours=2),
                "exp": now - timedelta(hours=1),
            },
            _settings().auth_jwt_secret,
            algorithm="HS256",
        )
        with pytest.raises(AuthenticationError):
            await service.verify(expired)

    @pytest.mark.asyncio
    async def test_wrong_issuer_rejected(self) -> None:
        token = security.JwtTokenService(
            _settings(auth_jwt_issuer="someone-else")
        ).issue_access_token(
            user_id="u",
            organization_id=None,
            roles=(),
            permissions=(),
            display_name="x",
            session_id="s",
        )
        with pytest.raises(AuthenticationError):
            await security.JwtTokenService(_settings()).verify(token)
