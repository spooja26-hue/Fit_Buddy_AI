from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import APP_NAME, BASE_DIR
from .database import init_db
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=APP_NAME,
    description=(
        "AI-powered fitness plan generator using "
        "Google Gemini."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# Serve CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static",
)


# Register application routes
app.include_router(router)