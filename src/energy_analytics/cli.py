import argparse

from energy_analytics.ingestion.sources import fetch_day_ahead_prices
from energy_analytics.ingestion.load_raw import load_day_ahead_prices

def ingest() -> None:
    df = fetch_day_ahead_prices()
    print(df.head())
    load_day_ahead_prices(df)

def main() -> None:
    parser = argparse.ArgumentParser(prog="project")
    parser.add_argument("command", choices=["ingest"])
    args = parser.parse_args()
    if args.command == "ingest":
        ingest()

if __name__ == "__main__":
    main()