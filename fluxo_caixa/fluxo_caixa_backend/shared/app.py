import logging
import uuid
from fastapi import FastAPI, Request
from .config import get_settings
from .errors import unhandled_exception_handler

settings = get_settings()

def create_app(title: str) -> FastAPI:
    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
    app = FastAPI(
        title=title,
        version="1.0.0",
        docs_url="/docs" if settings.environment != "prod" else None,
        redoc_url=None if settings.environment == "prod" else "/redoc",
    )

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    app.add_exception_handler(Exception, unhandled_exception_handler)
    return app
