"""Project ATLAS backend entrypoint.

Governing documents: IP-001 §7 (FastAPI runtime), §15 (Uvicorn ASGI server).

Run from the ``backend/`` directory:

    uv run uvicorn main:app --host 0.0.0.0 --port 8000

The module exposes ``app`` for the ASGI server and supports direct
execution for local development.
"""

from __future__ import annotations

from core.application import create_app

app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = app.state.container.settings
    uvicorn.run(app, host=settings.host, port=settings.port, log_config=None)
