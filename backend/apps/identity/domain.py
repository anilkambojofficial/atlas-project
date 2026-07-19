"""Identity domain rules — framework-free (RA-001 domain layer).

Governing documents:
- BP-003 §8.9 — permission model; deny by default.
- ES-004 §7 — password policy enforced at the domain boundary.
- CON-001 §5.5 — no framework imports here.
"""

from __future__ import annotations

from shared.exceptions import ValidationError

# --- Permission catalog (``<domain>.<resource>.<action>``) ---------------

PERM_USER_READ = "identity.user.read"
PERM_USER_MANAGE = "identity.user.manage"
PERM_ORG_READ = "identity.organization.read"
PERM_ORG_MANAGE = "identity.organization.manage"
PERM_MEMBER_READ = "identity.membership.read"
PERM_MEMBER_MANAGE = "identity.membership.manage"
PERM_ROLE_MANAGE = "identity.role.manage"

ALL_PERMISSIONS = (
    PERM_USER_READ,
    PERM_USER_MANAGE,
    PERM_ORG_READ,
    PERM_ORG_MANAGE,
    PERM_MEMBER_READ,
    PERM_MEMBER_MANAGE,
    PERM_ROLE_MANAGE,
)

#: System roles seeded for every organization (BP-003 §8.9).
SYSTEM_ROLES: dict[str, tuple[str, ...]] = {
    "owner": ALL_PERMISSIONS,
    "admin": (
        PERM_USER_READ,
        PERM_ORG_READ,
        PERM_MEMBER_READ,
        PERM_MEMBER_MANAGE,
        PERM_ROLE_MANAGE,
    ),
    "member": (PERM_USER_READ, PERM_ORG_READ, PERM_MEMBER_READ),
}


def validate_password_policy(password: str, *, min_length: int) -> None:
    """ES-004 §7 password policy; raises the platform validation error."""
    issues: list[dict[str, str]] = []
    if len(password) < min_length:
        issues.append(
            {"field": "password", "issue": f"must be at least {min_length} characters"}
        )
    if password.lower() == password or password.upper() == password:
        issues.append(
            {"field": "password", "issue": "must mix upper- and lower-case letters"}
        )
    if not any(ch.isdigit() for ch in password):
        issues.append({"field": "password", "issue": "must contain a digit"})
    if issues:
        raise ValidationError("Password does not meet the policy.", details=issues)


def validate_organization_slug(slug: str) -> None:
    """Slugs are DNS-label-like: lowercase alphanumerics and hyphens."""
    if not slug or len(slug) > 100 or not all(
        ch.isalnum() or ch == "-" for ch in slug
    ) or slug != slug.lower() or slug.startswith("-") or slug.endswith("-"):
        raise ValidationError(
            "Invalid organization slug.",
            details=[
                {
                    "field": "slug",
                    "issue": "lowercase letters, digits and inner hyphens only",
                }
            ],
        )
