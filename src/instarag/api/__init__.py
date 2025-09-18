import os
import sys
from pathlib import Path
import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from rich.console import Console

from .router import app_router as main_router
from .web.routes import router as web_router
from .utils import get_private_ip
from .constants import DEFAULT_APP_DETAILS

console = Console()

# Custom log format for Uvicorn
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(asctime)s] [%(levelname)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "custom": {
            "format": "[%(asctime)s] 🚀 %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
        "rich_console": {
            "formatter": "custom",
            "class": "rich.logging.RichHandler",
            "rich_tracebacks": True,
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["rich_console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["rich_console"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["rich_console"],
            "propagate": False,
        },
    },
}

# Apply custom log config
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events using FastAPI lifespan."""

    port = app.state.port
    private_ip = await get_private_ip()

    console.rule("[bold blue]🚀 InstaRAG Server Startup[/bold blue]")
    console.print("[bold green]✅ Application startup complete.[/bold green]")
    console.print("\n[bold cyan]🌍 Access the API at:[/bold cyan]")
    console.print(f"🔹 [bold white]Local:[/bold white]      http://localhost:{port}")
    if private_ip:
        console.print(
            f"🔹 [bold white]Network:[/bold white]    http://{private_ip}:{port}"
        )
    console.print(
        "\n[bold yellow]🚀 Welcome to InstaRAG! Your AI-powered retrieval system is ready.[/bold yellow]\n"
    )

    # Update Swagger UI metadata dynamically
    if hasattr(app.state, "configuration"):
        openapi_schema = app.openapi()
        openapi_schema["info"]["title"] = getattr(app.state.configuration, "title")
        openapi_schema["info"]["description"] = getattr(
            app.state.configuration, "description"
        )
        openapi_schema["info"]["version"] = getattr(app.state.configuration, "version")

    app.openapi_schema = openapi_schema

    yield  # Hand control to the FastAPI app

    # Shutdown process
    console.print("[bold red]🛑 Shutting down application.[/bold red]")


# Attach lifespan event to FastAPI
# Note :- Need to add license_info
app = FastAPI(
    title=DEFAULT_APP_DETAILS.TITLE.value,
    description=DEFAULT_APP_DETAILS.DESCRIPTION.value,
    version=DEFAULT_APP_DETAILS.VERSION.value,
    docs_url="/api/docs",  # Change Swagger UI URL
    redoc_url="/api/redoc",  # Change ReDoc URL
    openapi_url="/api/openapi.json",  # Change OpenAPI JSON URL
    lifespan=lifespan,
)

# Include include static files
BASE_DIR = Path(__file__).resolve().parent
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / os.path.join("web", "static"))),
    name="static",
)


app.include_router(web_router, prefix="", tags=["Web Interface"])
app.include_router(main_router, prefix="/api", tags=["Backend Service"])
