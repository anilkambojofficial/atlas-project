"""Identity & Access contracts — interfaces only.

Governing documents:
- BP-003 §4.1/§8 — the Identity & Access capability surface: identity
  classes (Interactive/Human, Machine, Agent — §8.3–§8.5), the central
  Policy Decision Point (§8.9), and the reusable Policy Enforcement
  Point contract every downstream service embeds (§8.10).
- RA-011 §5 — identity types; §7 — centralized, auditable authorization
  decisions (permit/deny with obligations).
- BP-003 ED-005 — enforcement is fail-closed: absence of a decision is
  a deny; the PEP implementation delivered by IP-002 enforces this.

No cryptography, token parsing, or policy evaluation lives here —
that is IP-002 scope (approved S1.4 decision: interfaces only).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol, runtime_checkable


class IdentityClass(str, Enum):
    """The three authenticated identity classes (BP-003 §8.3–§8.5)."""

    HUMAN = "human"
    MACHINE = "machine"
    AGENT = "agent"


@dataclass(frozen=True)
class Principal:
    """An authenticated identity assertion (BP-003 §5.2, RA-011 §5)."""

    subject_id: str
    identity_class: IdentityClass
    organization_id: str | None
    roles: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()
    display_name: str | None = None


@dataclass(frozen=True)
class AccessDecision:
    """A Policy Decision Point verdict (RA-011 §7: permit/deny/obligations)."""

    permit: bool
    reason: str
    obligations: tuple[str, ...] = field(default=())


@runtime_checkable
class TokenVerifier(Protocol):
    """Verifies a bearer credential into a :class:`Principal`.

    Implementations (IP-002 Token Service) raise the platform
    ``AuthenticationError`` on invalid, expired, or revoked credentials.
    """

    async def verify(self, token: str) -> Principal:  # pragma: no cover
        ...


@runtime_checkable
class PolicyDecisionPoint(Protocol):
    """Central authorization decision surface (BP-003 §8.9).

    Every downstream service consumes decisions through this contract;
    embedding authorization logic in services is prohibited (BP-003 ED-002).
    """

    async def authorize(
        self,
        principal: Principal,
        *,
        resource: str,
        action: str,
        organization_id: str | None = None,
    ) -> AccessDecision:  # pragma: no cover
        ...
