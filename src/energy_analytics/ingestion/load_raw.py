import pandas as pd

from energy_analytics.db import get_connection
from energy_analytics.ingestion.sources import Dataset


def load_dataset(dataset: Dataset, df: pd.DataFrame) -> None:
    con = get_connection()
    pk = ", ".join(dataset.primary_key)

    # First run: create the table with the same columns as the DataFrame
    con.execute(f"CREATE TABLE IF NOT EXISTS {dataset.table} AS SELECT * FROM df LIMIT 0")
    con.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS ux_{dataset.table.replace('.', '_')} ON {dataset.table} ({pk})")

    # Upsert: replace rows with the same primary key, insert the rest
    con.execute(f"INSERT OR REPLACE INTO {dataset.table} SELECT * FROM df")

    total = con.execute(f"SELECT COUNT(*) FROM {dataset.table}").fetchone()[0]
    print(f"Loaded {len(df)} rows. {dataset.table} now has {total} rows.")
    con.close()