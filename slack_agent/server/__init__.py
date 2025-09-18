"""Server package for Slack Agent."""

from .app import create_fastapi_app

__all__ = ["create_fastapi_app"]
