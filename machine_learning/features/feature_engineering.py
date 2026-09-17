"""
machine_learning/features/feature_engineering.py

Turns the two raw sources into the pooled, direct multi-horizon modelling
table. See docs/METHODOLOGY.md for the full reasoning; the essentials:

1. COLLAPSE: the raw country panel stores one row per country per calendar DAY,
   but the monthly measures repeat across every day of the month. We collapse
   to one row per (country, year, month) -- with an integrity assertion, since
   the repo's original data/README.md mis-described this.

2. ORIGIN-ANCHORED ARRIVALS FEATURES: lags, rolling means, growth are built
   from data strictly at/before the forecast origin. No future target leaks in.

3. AVAILABILITY-AWARE EXOGENOUS SOURCING: each macro/GPR/fuel/FX predictor is
   sourced from the freshest month that would ACTUALLY have been published by
   the simulated present (origin + arrivals-publication-lag), using each
   variable's own lag from config.VARIABLE_LAGS. This replaces an arbitrary
   fixed "gap" -- the validation reflects real publication timing.

4. HORIZON TABLE: one row per (country, origin, horizon in 1..4). `horizon` is
   an explicit feature (pooled direct multi-horizon design).
"""

import numpy as np
import pandas as pd

from .. import config
from ..data_loader import load_country_panel, load_macro_series

MACRO_FEATURE_COLS = [
    "gpr_global_index", "gpr_malaysia_index", "brent_crude_usd_bbl",
    "leading_index", "coincident_index", "lagging_index",
    "leading_diffusion_index", "coincident_diffusion_index",
    "ron95_rm_litre_monthly_avg", "ron97_rm_litre_monthly_avg",
    "diesel_peninsular_rm_litre_monthly_avg", "diesel_east_malaysia_rm_litre_monthly_avg",
]
PANEL_KEEP = ["source_country_iso3", "source_country_name", "source_currency_code",
              "market_segment", "year", "month", "monthly_tourist_arrivals",
              "monthly_myr_per_source_currency", "target_missing_flag", "model_row_status"]
ID_COLS = ["source_country_iso3", "source_country_name", "market_segment", "period"]
ORIGIN_LAG_COLS = ["arrivals_lag_1m", "arrivals_lag_2m", "arrivals_lag_3m",
                   "arrivals_lag_6m", "arrivals_lag_12m"]


def build_monthly_panel(prefer_db=True) -> pd.DataFrame:
    """Collapse daily rows to country-month and merge national macro series."""
    panel_raw = load_country_panel(prefer_db)
    panel_raw["date"] = pd.to_datetime(panel_raw["date"])
    grp = ["source_country_iso3", "year", "month"]
    chk = panel_raw.groupby(grp).agg(t=("monthly_tourist_arrivals", "nunique"),
                                      fx=("monthly_myr_per_source_currency", "nunique"))
    assert (chk["t"] <= 1).all() and (chk["fx"] <= 1).all(), \
        "Monthly values vary within a month -- daily-collapse assumption violated."
    monthly = (panel_raw.sort_values(grp).drop_duplicates(grp, keep="first")[PANEL_KEEP]
               .reset_index(drop=True))

    macro = load_macro_series(prefer_db)
    macro = macro[["year", "month_number"] + MACRO_FEATURE_COLS].rename(columns={"month_number": "month"})
    df = monthly.merge(macro, on=["year", "month"], how="left")
    df["period"] = pd.to_datetime(dict(year=df.year, month=df.month, day=1))
    return df.sort_values(["source_country_iso3", "period"]).reset_index(drop=True)


def _add_origin_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    tgt = df.groupby("source_country_iso3")["monthly_tourist_arrivals"]
    for lag in (1, 2, 3, 6, 12):
        df[f"arrivals_lag_{lag}m"] = tgt.shift(lag)
    return df


def build_horizon_table(prefer_db=True, origins_filter=None, L_arrivals=None) -> pd.DataFrame:
    """Build the (country, origin, horizon) modelling table.

    origins_filter: optional list/Index of origin `period` timestamps to
        restrict to (e.g. the single live origin). None = all origins.
    L_arrivals: arrivals publication lag; defaults to config primary.
    """
    if L_arrivals is None:
        L_arrivals = config.L_ARRIVALS_PRIMARY
    full = _add_origin_features(build_monthly_panel(prefer_db))

    origins = full if origins_filter is None else full[full["period"].isin(origins_filter)]
    fp = full.set_index(["source_country_iso3", "period"])
    tgt_by_key = full.set_index(["source_country_iso3", "period"])["monthly_tourist_arrivals"]
    per_country = {c: g.sort_values("period").reset_index(drop=True)
                   for c, g in full.groupby("source_country_iso3")}

    rows = []
    for _, r in origins.iterrows():
        country = r["source_country_iso3"]
        present = r["period"] + pd.DateOffset(months=L_arrivals)
        trailing = per_country[country].loc[per_country[country]["period"] <= r["period"],
                                            "monthly_tourist_arrivals"]
        snap = {c: r[c] for c in ORIGIN_LAG_COLS}
        snap["origin_arrivals"] = r["monthly_tourist_arrivals"]
        roll3, roll6 = trailing.tail(3).mean(), trailing.tail(6).mean()

        for h in config.HORIZONS:
            target_period = r["period"] + pd.DateOffset(months=h)
            row = {c: r[c] for c in ID_COLS}
            row.update(snap)
            row["origin_roll_mean_3m"] = roll3
            row["origin_roll_mean_6m"] = roll6
            row["yoy_growth"] = ((snap["origin_arrivals"] - snap["arrivals_lag_12m"])
                                 / snap["arrivals_lag_12m"]) if snap["arrivals_lag_12m"] else np.nan
            # availability-aware exogenous sourcing
            for var, lag in config.VARIABLE_LAGS.items():
                available_through = present - pd.DateOffset(months=lag)
                source_month = min(target_period - pd.DateOffset(months=1), available_through)
                key = (country, source_month)
                row[var] = fp.loc[key, var] if key in fp.index else np.nan
            # seasonal-naive reference (target - 12m), leakage-safe
            row["seasonal_naive_target"] = tgt_by_key.get(
                (country, target_period - pd.DateOffset(months=12)), np.nan)
            row["horizon"] = h
            row["L_arrivals"] = L_arrivals
            row["target_period"] = target_period
            row["target_month_sin"] = np.sin(2 * np.pi * target_period.month / 12)
            row["target_month_cos"] = np.cos(2 * np.pi * target_period.month / 12)
            row["target_arrivals"] = tgt_by_key.get((country, target_period), np.nan)
            row["model_row_status"] = r["model_row_status"]
            rows.append(row)
    return pd.DataFrame(rows)


def split_train_and_live(horizon_table: pd.DataFrame):
    """Return (train_rows, live_rows).

    train_rows: every (origin, horizon) row whose target month is published.
    live_rows : the 80 rows that forecast the unpublished months. These come
        from the LAST ACTUAL origin projected forward h=1..4 (so their targets
        land on the 4 unpublished months) -- NOT from hold-out months used as
        origins (which would have no valid arrivals history to anchor on and
        would produce 80x4=320 rows). We select them as the rows whose target
        month has no published actual AND whose origin is the last actual month.
    """
    # Training rows: published target AND full lag history (drop the first 12
    # "cold start" months per country, which lack arrivals_lag_12m). This
    # matches the finalized model exactly -- LightGBM tolerates NaN lags, so
    # without this filter the model would silently train on partial-history
    # rows and produce different forecasts.
    train = horizon_table[horizon_table["target_arrivals"].notna()
                          & horizon_table["arrivals_lag_12m"].notna()].copy()

    # last origin that is itself a training-eligible (published) month
    published_origins = horizon_table.loc[
        horizon_table["model_row_status"] == "Training eligible", "period"]
    last_actual_origin = published_origins.max()
    live = horizon_table[(horizon_table["period"] == last_actual_origin)
                         & (horizon_table["target_arrivals"].isna())].copy()
    return train, live


def make_backtest_fold(horizon_table: pd.DataFrame, val_origin):
    """Row-level, availability-aware fold: a training row is usable iff its own
    target month is known by val_origin (no arbitrary gap)."""
    vo = pd.Timestamp(val_origin)
    train = horizon_table[(horizon_table["target_period"] <= vo)
                          & (horizon_table["target_arrivals"].notna())]
    val = horizon_table[(horizon_table["period"] == vo)
                        & (horizon_table["target_arrivals"].notna())]
    return train, val
