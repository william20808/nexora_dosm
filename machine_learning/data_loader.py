"""
machine_learning/data_loader.py

Loads the two raw sources (country panel, national time series) from the repo
SQLite DB, falling back to the .xlsx workbook if the DB is absent. Returns the
raw frames unchanged; all cleaning/collapsing happens in
feature_engineering.py so the loader has one job only.
"""

import sqlite3
import pandas as pd

from . import config


def _read(source_pair, prefer_db=True):
    table_name, sheet_name = source_pair
    if prefer_db and config.DB_PATH.exists():
        con = sqlite3.connect(config.DB_PATH)
        try:
            return pd.read_sql(f"SELECT * FROM {table_name}", con)
        finally:
            con.close()
    if config.XLSX_FALLBACK.exists():
        return pd.read_excel(config.XLSX_FALLBACK, sheet_name=sheet_name)
    raise FileNotFoundError(
        f"Neither {config.DB_PATH} nor {config.XLSX_FALLBACK} found. "
        "Place the dataset in data/ before running the ML pipeline."
    )


def load_country_panel(prefer_db=True) -> pd.DataFrame:
    return _read(config.PANEL_SOURCE, prefer_db)


def load_macro_series(prefer_db=True) -> pd.DataFrame:
    return _read(config.MACRO_SOURCE, prefer_db)
