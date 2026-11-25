import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

API_TOKEN = os.getenv("ENTSOE_API_TOKEN")
DB_PATH = ROOT / "data" / "warehouse.duckdb"

COUNTRY_CODE = "DE_LU"
DAYS_BACK = 3