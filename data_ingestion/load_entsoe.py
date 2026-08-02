"""
ENTSO-E ingestion script.

Pulls day-ahead electricity prices for Germany (DE_LU) for the last N days
and lands the raw data into a DuckDB table (bronze layer).

"""

from pathlib import Path
from datetime import datetime, timedelta, timezone

import duckdb
import pandas as pd
from dotenv import load_dotenv
from entsoe import EntsoePandasClient
import os


# Load environment variables (.env one level up from this script)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_TOKEN = os.getenv("ENTSOE_API_TOKEN")
if not API_TOKEN:
    raise ValueError("ENTSOE_API_TOKEN not found. Check your .env file.")


COUNTRY_CODE = "DE_LU"          # Germany + Luxembourg bidding zone
DAYS_BACK = 3                   # how far back to pull
DB_PATH = Path(__file__).resolve().parent.parent / "dev.duckdb"
TABLE_NAME = "raw_entsoe_day_ahead_prices"


def fetch_day_ahead_prices() -> pd.DataFrame:
    client = EntsoePandasClient(api_key=API_TOKEN)

    end = pd.Timestamp.now(tz="Europe/Berlin")
    start = end - timedelta(days=DAYS_BACK)

    # Returns a pandas Series indexed by timestamp
    prices = client.query_day_ahead_prices(COUNTRY_CODE, start=start, end=end)

    # Convert to a tidy DataFrame for storage
    df = prices.reset_index()
    df.columns = ["timestamp", "price_eur_mwh"]
    df["country_code"] = COUNTRY_CODE
    df["ingested_at"] = datetime.now(timezone.utc)

    return df


def load_to_duckdb(df: pd.DataFrame) -> None:
    con = duckdb.connect(str(DB_PATH))

    # Create table on first run, otherwise append new rows
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            timestamp TIMESTAMP,
            price_eur_mwh DOUBLE,
            country_code VARCHAR,
            ingested_at TIMESTAMP
        )
    """)

    con.execute(f"INSERT INTO {TABLE_NAME} SELECT * FROM df")

    row_count = con.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    print(f"Loaded {len(df)} rows. Table '{TABLE_NAME}' now has {row_count} total rows.")

    con.close()


if __name__ == "__main__":
    print(f"Fetching day-ahead prices for {COUNTRY_CODE}, last {DAYS_BACK} days...")
    data = fetch_day_ahead_prices()
    print(data.head())

    print(f"Writing to DuckDB at: {DB_PATH}")
    load_to_duckdb(data)

