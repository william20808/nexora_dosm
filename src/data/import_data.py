"""
import_data.py

Ingests the monthly shared predictors dataset from Excel into the SQLite database.
Reads all four sheets from 'database/monthly_shared_predictors_corrected_mar2017.xlsx',
cleans/formats date columns for SQLite compatibility, populates 'database/dosm_datathon.db',
creates helpful indices for queries, and updates 'database/schema.sql'.
"""

import os
import sqlite3
import pandas as pd
from pathlib import Path


def get_base_dir() -> Path:
    """Returns repository root directory."""
    return Path(__file__).resolve().parent.parent.parent


def ingest_excel_to_sqlite(
    excel_path: Path | None = None,
    db_path: Path | None = None,
    schema_sql_path: Path | None = None,
):
    base_dir = get_base_dir()
    if excel_path is None:
        excel_path = base_dir / "database" / "monthly_shared_predictors_corrected_mar2017.xlsx"
    if db_path is None:
        db_path = base_dir / "database" / "dosm_datathon.db"
    if schema_sql_path is None:
        schema_sql_path = base_dir / "database" / "schema.sql"

    print(f"Reading Excel from: {excel_path}")
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found at {excel_path}")

    sheets_mapping = {
        "Imputed Time Series Data": "imputed_time_series_data",
        "Original Data": "original_time_series_data",
        "Imputed Panel Data (2)": "imputed_panel_data",
        "Original Data (2)": "original_panel_data",
    }

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Drop legacy placeholder tables if present
    cursor.execute("DROP TABLE IF EXISTS athlete_training")
    conn.commit()

    for sheet_name, table_name in sheets_mapping.items():
        print(f"Loading sheet '{sheet_name}' into table '{table_name}'...")
        df = pd.read_excel(excel_path, sheet_name=sheet_name)

        # Standardize date columns to ISO format string (YYYY-MM-DD)
        for col in ["month", "date"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")

        # Drop table if exists to replace cleanly
        cursor.execute(f"DROP TABLE IF EXISTS [{table_name}]")
        conn.commit()

        # Write dataframe to SQLite
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"  -> Inserted {len(df):,} rows and {len(df.columns)} columns into '{table_name}'.")

    # Create helpful indices for performance and queries
    print("Creating indices on key query dimensions...")
    indices = [
        ("idx_its_year_month", "imputed_time_series_data", ["year", "month_number"]),
        ("idx_its_month", "imputed_time_series_data", ["month"]),
        ("idx_ots_year_month", "original_time_series_data", ["year", "month_number"]),
        ("idx_ots_month", "original_time_series_data", ["month"]),
        ("idx_ipd_country_date", "imputed_panel_data", ["source_country_iso3", "date"]),
        ("idx_ipd_country_year_month", "imputed_panel_data", ["source_country_iso3", "year", "month"]),
        ("idx_opd_country_date", "original_panel_data", ["source_country_iso3", "date"]),
        ("idx_opd_country_year_month", "original_panel_data", ["source_country_iso3", "year", "month"]),
    ]

    for idx_name, table_name, cols in indices:
        cols_str = ", ".join(f"[{c}]" for c in cols)
        cursor.execute(f"CREATE INDEX IF NOT EXISTS [{idx_name}] ON [{table_name}] ({cols_str});")
    conn.commit()

    # Generate schema.sql from sqlite_master
    print(f"Updating schema documentation at {schema_sql_path}...")
    cursor.execute(
        "SELECT type, name, sql FROM sqlite_master WHERE type IN ('table', 'index') AND name NOT LIKE 'sqlite_%' ORDER BY type DESC, name"
    )
    schema_entries = cursor.fetchall()
    with open(schema_sql_path, "w", encoding="utf-8") as f:
        f.write("-- Schema for DOSM Tourism Datathon Database (dosm_datathon.db)\n")
        f.write("-- Generated from monthly_shared_predictors_corrected_mar2017.xlsx\n\n")
        for item_type, item_name, sql in schema_entries:
            if sql:
                f.write(f"-- {item_type.upper()}: {item_name}\n")
                f.write(f"{sql};\n\n")

    conn.close()
    print("Database ingestion and schema update completed successfully!")


if __name__ == "__main__":
    ingest_excel_to_sqlite()
