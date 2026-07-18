"""Shared authentication/authorization contracts (IP-001 §9 — auth package).

Interfaces only, per the approved S1.4 decision: BP-003 defines the
Identity & Access surfaces (three identity classes, PDP/PEP); IP-002
implements them inside ``apps/identity``. Downstream services depend on
these contracts, never on the implementation (IP-001 §11).
"""

from shared.auth.contracts import (
    AccessDecision,
    IdentityClass,
    PolicyDecisionPoint,
    Principal,
    TokenVerifier,
)

__all__ = [
    "AccessDecision",
    "IdentityClass",
    "PolicyDecisionPoint",
    "Principal",
    "TokenVerifier",
]
