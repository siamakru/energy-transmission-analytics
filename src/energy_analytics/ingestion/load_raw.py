import pandas as pd
from energy_analytics.db import get_connection

TABLE = "raw.entsoe_day_ahead_prices"

def load_day_ahead_prices(df: pd.DataFrame) -> None:
    con = get_connection()
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            timestamp TIMESTAMPTZ,
            price_eur_mwh DOUBLE,
            country_code VARCHAR,
            ingested_at TIMESTAMPTZ,
            PRIMARY KEY (timestamp, country_code)
        )
    """)
    con.execute(f"""
        INSERT OR REPLACE INTO {TABLE}
        SELECT timestamp, price_eur_mwh, country_code, ingested_at FROM df
    """)
    total = con.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
    print(f"Loaded {len(df)} rows. {TABLE} now has {total} rows.")
    con.close()