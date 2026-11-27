ingest:
	python -m energy_analytics.cli ingest

duckdb_ui:
	duckdb -ui data/warehouse.duckdb

duckdb_tables:
	duckdb data/warehouse.duckdb -readonly -c "SHOW ALL TABLES"

