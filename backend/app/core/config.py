import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DB_PATH = PROJECT_ROOT / "database" / "mars_explorer.db"

class Settings:
    PROJECT_NAME: str = "MARS EXPLORER — AI-Powered Interplanetary Survival & Mission Planning System"
    VERSION: str = "1.0.0"
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")
    CORS_ORIGINS: list[str] = [
        o.strip() for o in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000,*"
        ).split(",") if o.strip()
    ]
    NASA_MARS_TREK_WMTS_BASE: str = os.getenv(
        "NASA_MARS_TREK_WMTS_BASE", "https://trek.nasa.gov/tiles/Mars/EQ"
    )
    DATA_DIR: Path = PROJECT_ROOT / "data"

settings = Settings()
