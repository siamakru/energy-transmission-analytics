from datetime import datetime, timedelta, timezone

import pandas as pd
from entsoe import EntsoePandasClient

from energy_analytics.config import API_TOKEN, COUNTRY_CODE, DAYS_BACK

def fetch_day_ahead_prices() -> pd.DataFrame:
    if not API_TOKEN:
        raise ValueError("ENTSOE_API_TOKEN not found. Check your .env file.")

    client = EntsoePandasClient(api_key=API_TOKEN)
    end = pd.Timestamp.now(tz="Europe/Berlin")
    start = end - timedelta(days=DAYS_BACK)

    prices = client.query_day_ahead_prices(COUNTRY_CODE, start=start, end=end)

    df = prices.reset_index()
    df.columns = ["timestamp", "price_eur_mwh"]
    df["country_code"] = COUNTRY_CODE
    df["ingested_at"] = datetime.now(timezone.utc)
    return df