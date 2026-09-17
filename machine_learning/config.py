"""
machine_learning/config.py

Single source of truth for paths, the locked feature set, model
hyperparameters, and the publication-lag assumptions. Every other module
imports from here so there is exactly one place to change a setting.

Data is read from the repository's SQLite database (data/dosm_datathon.db),
which is the reproducible source committed to the repo. An .xlsx fallback is
supported for local experimentation but the DB is authoritative.
"""

from pathlib import Path

# --- Paths (resolved relative to the repo root, two levels up from this file) ---
REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "data" / "dosm_datathon.db"
XLSX_FALLBACK = REPO_ROOT / "data" / "final_deliveries_dataset.xlsx"

ML_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = ML_DIR / "artifacts"
OUTPUT_DIR = ML_DIR / "outputs"

# --- Table / sheet names (DB table name, xlsx sheet name) ---
PANEL_SOURCE = ("imputed_panel_data", "Imputed Country Panel Data")
MACRO_SOURCE = ("imputed_time_series_data", "Imputed Time Series Data")

# --- Locked modelling design (see report methodology) -----------------------
# Direct multi-horizon: predict 1..4 months ahead, horizon is a feature.
HORIZONS = (1, 2, 3, 4)
MAX_HORIZON = max(HORIZONS)

# Arrivals publication lag is an ASSUMPTION (no verified release archive).
# Primary run uses 4; 3 is reported as a sensitivity check.
L_ARRIVALS_PRIMARY = 4
L_ARRIVALS_SENSITIVITY = 3

# Per-variable publication lags (months). See report:
# "documented publication schedules where available and conservative lag
#  assumptions where exact release timing could not be verified."
VARIABLE_LAGS = {
    "gpr_global_index": 1, "gpr_malaysia_index": 1, "brent_crude_usd_bbl": 1,
    "leading_index": 3, "coincident_index": 3, "lagging_index": 3,
    "leading_diffusion_index": 3, "coincident_diffusion_index": 3,
    "ron95_rm_litre_monthly_avg": 0, "ron97_rm_litre_monthly_avg": 0,
    "diesel_peninsular_rm_litre_monthly_avg": 0, "diesel_east_malaysia_rm_litre_monthly_avg": 0,
    "monthly_myr_per_source_currency": 0,
}

# --- Locked 19-feature set + 1 categorical input (source_country_iso3) -------
FINAL_FEATURES = [
    "arrivals_lag_1m", "arrivals_lag_2m", "arrivals_lag_3m", "arrivals_lag_6m", "arrivals_lag_12m",
    "origin_arrivals", "origin_roll_mean_3m", "origin_roll_mean_6m", "yoy_growth",
    "target_month_sin", "target_month_cos", "horizon", "seasonal_naive_target",
    "gpr_global_index", "gpr_malaysia_index", "brent_crude_usd_bbl",
    "ron97_rm_litre_monthly_avg", "diesel_peninsular_rm_litre_monthly_avg",
    "monthly_myr_per_source_currency",
]
CATEGORICAL_FEATURE = "source_country_iso3"

# --- Backtest folds (rolling-origin) ----------------------------------------
PRIMARY_FOLDS = ["2023-03-01", "2023-09-01", "2024-03-01", "2024-09-01", "2025-09-01"]
STRESS_FOLDS = ["2020-03-01", "2020-09-01", "2021-03-01", "2021-09-01", "2022-03-01"]

# --- LightGBM hyperparameters (locked) --------------------------------------
LGBM_PARAMS = dict(
    n_estimators=300, max_depth=4, learning_rate=0.05,
    min_child_samples=20, verbosity=-1, random_state=42,
)
RIDGE_ALPHA = 100.0
RIDGE_REFERENCE_COUNTRY = "USA"  # dropped category -> identifiable GPR x country
RANDOM_SEED = 42
