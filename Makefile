ingest:
	python -m energy_analytics.cli ingest

duckdb_ui:
	duckdb -ui data/warehouse.duckdb

duckdb_tables:
	duckdb data/warehouse.duckdb -readonly -c "SHOW ALL TABLES"

power_on_job:
	sudo pmset repeat wakeorpoweron MTWRFSU 18:55:00 sleep MTWRFSU 19:15:00

power_on_job_cancel:
	sudo pmset repeat cancel

