from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import get_settings
from app.database import init_db
from app.routers import (
    contact_router,
    property_finder_router,
    materials_router,
    partners_router,
    quote_router,
    admin_router,
)

settings = get_settings()

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifecycle ──────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting SSR Group Backend...")
    await init_db()
    logger.info("✅ Database tables created")
    yield
    logger.info("👋 Shutting down SSR Group Backend")


# ── App ────────────────────────────────────────────────

app = FastAPI(
    title="SSR Group API",
    description="Backend API for SSR Group — Construction & Real Estate (ssrgroupcivil.in)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global Error Handler ──────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Something went wrong. Please try again."},
    )


# ── Routes ─────────────────────────────────────────────

API_PREFIX = "/api/v1"

app.include_router(contact_router, prefix=API_PREFIX)
app.include_router(property_finder_router, prefix=API_PREFIX)
app.include_router(materials_router, prefix=API_PREFIX)
app.include_router(partners_router, prefix=API_PREFIX)
app.include_router(quote_router, prefix=API_PREFIX)
app.include_router(admin_router, prefix=API_PREFIX)


@app.get("/")
async def root():
    return {
        "name": "SSR Group API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
