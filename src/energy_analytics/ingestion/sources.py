from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

import pandas as pd
from entsoe import EntsoePandasClient

from energy_analytics.config import API_TOKEN, COUNTRY_CODE


@dataclass
class Dataset:
    fetch: Callable[[pd.Timestamp, pd.Timestamp], pd.DataFrame]
    table: str
    primary_key: list[str]


def _client() -> EntsoePandasClient:
    if not API_TOKEN:
        raise ValueError("ENTSOE_API_TOKEN not found. Check your .env file.")
    return EntsoePandasClient(api_key=API_TOKEN)


def _finish(df: pd.DataFrame) -> pd.DataFrame:
    df["country_code"] = COUNTRY_CODE
    df["ingested_at"] = datetime.now(timezone.utc)
    return df


# --- one fetch function per dataset ---
def fetch_day_ahead_prices(start, end) -> pd.DataFrame:
    prices = _client().query_day_ahead_prices(COUNTRY_CODE, start=start, end=end)
    df = prices.reset_index()
    df.columns = ["timestamp", "price_eur_mwh"]
    return _finish(df)


def fetch_load(start, end) -> pd.DataFrame:
    raw = _client().query_load_and_forecast(COUNTRY_CODE, start=start, end=end)
    raw.index.name = "timestamp"
    df = raw.reset_index().rename(columns={
        "Forecasted Load": "forecast_load_mw",
        "Actual Load": "actual_load_mw",
    })
    return _finish(df)


DATASETS = {
    "day_ahead_prices": Dataset(fetch_day_ahead_prices, "raw.entsoe_day_ahead_prices", ["timestamp", "country_code"]),
    "load_and_forecast": Dataset(fetch_load, "raw.entsoe_load", ["timestamp", "country_code"]),
}