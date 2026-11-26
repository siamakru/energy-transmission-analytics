import argparse

import pandas as pd

from energy_analytics.ingestion.sources import DATASETS
from energy_analytics.ingestion.load_raw import load_dataset

TZ = "Europe/Berlin"


def ingest(name: str, start: pd.Timestamp, end: pd.Timestamp) -> None:
    dataset = DATASETS[name]
    df = dataset.fetch(start, end)
    print(df.head())
    load_dataset(dataset, df)


def main() -> None:
    parser = argparse.ArgumentParser(prog="energy-analytics")
    parser.add_argument("command", choices=["ingest"])
    parser.add_argument("--dataset", choices=[*DATASETS, "all"], default="all")
    parser.add_argument("--start", help="YYYY-MM-DD, default: 3 days ago")
    parser.add_argument("--end", help="YYYY-MM-DD, default: now")
    args = parser.parse_args()

    end = pd.Timestamp(args.end, tz=TZ) if args.end else pd.Timestamp.now(tz=TZ)
    start = pd.Timestamp(args.start, tz=TZ) if args.start else end - pd.Timedelta(days=3)

    if args.command == "ingest":
        names = list(DATASETS) if args.dataset == "all" else [args.dataset]
        for name in names:
            print(f"Ingesting {name}: {start} -> {end}")
            ingest(name, start, end)


if __name__ == "__main__":
    main()