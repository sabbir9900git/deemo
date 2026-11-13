"""
MARS EXPLORER — FastAPI Backend Entrypoint
AI-Powered Interplanetary Survival & Mission Planning System
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.services.seed_data import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "REST API for MARS EXPLORER integrating USGS Planetary Nomenclature, "
        "NASA Mars Trek / PDS scientific layers, MOLA terrain risk analysis, "
        "A* Marswalk surface route planning, and the Grounded AI Mission Assistant."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "application": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_prefix": "/api",
    }
