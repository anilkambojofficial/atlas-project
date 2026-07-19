"""Identity cryptography: password hashing and token services.

Governing documents:
- ES-004 §7 / BP-003 — Argon2id password hashing.
- BP-003 §8.7 — short-lived access tokens; opaque rotated refresh tokens.
- ADR-004 — verification failures reject (fail closed); the JWT verifier
  implements the platform ``shared.auth.TokenVerifier`` Protocol.
- ES-004 §12 — raw tokens are never persisted; refresh tokens store a
  SHA-256 hash only.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

from shared.auth import IdentityClass, Principal
from shared.config import Settings
from shared.exceptions import AuthenticationError

_hasher = PasswordHasher()  # argon2id with library-audited defaults


def hash_password(password: str) -> str:
    """Argon2id hash for storage (ES-004 §7)."""
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Constant-work verification; False on any mismatch or malformed hash."""
    try:
        return _hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, ValueError):
        return False


def password_needs_rehash(password_hash: str) -> bool:
    """True when parameters are outdated and a rehash-on-login is due."""
    try:
        return _hasher.check_needs_rehash(password_hash)
    except Exception:  # noqa: BLE001 — malformed hash: force rehash path
        return True


def new_opaque_token() -> str:
    """Cryptographically random opaque token (refresh / verification)."""
    return secrets.token_urlsafe(48)


def token_digest(token: str) -> str:
    """SHA-256 digest used for at-rest token storage (ES-004 §12)."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class JwtTokenService:
    """Issues and verifies platform access tokens.

    Structurally satisfies ``shared.auth.TokenVerifier`` — bound in the
    composition root (CON-001 §4.3), never imported by ``shared``.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def issue_access_token(
        self,
        *,
        user_id: str,
        organization_id: str | None,
        roles: tuple[str, ...],
        permissions: tuple[str, ...],
        display_name: str,
        session_id: str,
    ) -> str:
        now = datetime.now(timezone.utc)
        claims: dict[str, Any] = {
            "iss": self._settings.auth_jwt_issuer,
            "sub": user_id,
            "iat": now,
            "exp": now + timedelta(seconds=self._settings.auth_access_token_ttl_seconds),
            "org": organization_id,
            "roles": list(roles),
            "perms": list(permissions),
            "name": display_name,
            "sid": session_id,
            "cls": IdentityClass.HUMAN.value,
        }
        return jwt.encode(
            claims,
            self._settings.auth_jwt_secret,
            algorithm=self._settings.auth_jwt_algorithm,
        )

    async def verify(self, token: str) -> Principal:
        """``TokenVerifier`` implementation — fail closed (ADR-004 §2)."""
        try:
            claims = jwt.decode(
                token,
                self._settings.auth_jwt_secret,
                algorithms=[self._settings.auth_jwt_algorithm],
                issuer=self._settings.auth_jwt_issuer,
                options={"require": ["exp", "iat", "sub", "iss"]},
            )
        except jwt.PyJWTError as exc:
            raise AuthenticationError("Invalid or expired credentials.") from exc
        return Principal(
            subject_id=str(claims["sub"]),
            identity_class=IdentityClass(claims.get("cls", "human")),
            organization_id=claims.get("org"),
            roles=tuple(claims.get("roles", ())),
            permissions=tuple(claims.get("perms", ())),
            display_name=claims.get("name"),
        )
