"""Backend infrastructure layer (IP-001 §6 — ``backend/infrastructure/``).

Cross-service adapters for the platform data and messaging substrate:
PostgreSQL (SQLAlchemy 2.x), Redis, and Kafka, plus the persistence
patterns mandated by RA-001 (Repository, Unit of Work).

Per RA-001 §4 (dependency rule) this layer is consumed by application
services through the dependency-injection container; domain layers never
import infrastructure directly. No business logic lives here (ES-001 §3).
"""
