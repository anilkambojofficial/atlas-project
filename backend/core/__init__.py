"""Project ATLAS backend platform runtime (IP-001 §7, RA-001).

The ``core`` package owns the cross-cutting application runtime consumed
by every backend service: application factory, dependency-injection
container, middleware pipeline, centralized exception handling, and the
platform health-check registry. It contains no business logic — business
rules belong exclusively to service domain layers (ES-001 §3, RA-001 §5).
"""
