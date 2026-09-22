"""
machine_learning/models/predict.py

Loads the trained artifact and produces the Power BI handoff tables:
  - outputs/historical_actuals.csv   (one row per country-month; NO horizon)
  - outputs/forecast_future_2026.csv (the 80 live forecasts; horizon lives here)

Historical actuals are kept SEPARATE from anything horizon-indexed so a
dashboard can never double-count by summing a target month that repeats across
horizons. See machine_learning/README.md.

Run:  python -m machine_learning.models.predict
"""

import numpy as np
import pandas as pd
import joblib

from .. import config
from ..features.feature_engineering import (build_monthly_panel, build_horizon_table,
                                            split_train_and_live)

COVERAGE = "20 modelled source markets only; NOT all-Malaysia total"


def _load_artifact():
    path = config.ARTIFACT_DIR / "lightgbm_final.joblib"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run `python -m machine_learning.models.train` first.")
    return joblib.load(path)


def generate_outputs(prefer_db=True):
    art = _load_artifact()
    model = art["model"]
    feats = art["features"]

    # --- historical actuals: de-duplicated country-month, no horizon ---
    panel = build_monthly_panel(prefer_db)
    actuals = (panel[panel["model_row_status"] == "Training eligible"]
               [["source_country_iso3", "source_country_name", "market_segment",
                 "period", "year", "month", "monthly_tourist_arrivals"]]
               .drop_duplicates(["source_country_iso3", "period"])
               .rename(columns={"monthly_tourist_arrivals": "actual_arrivals"})
               .sort_values(["source_country_iso3", "period"]).reset_index(drop=True))
    actuals["period"] = actuals["period"].dt.strftime("%Y-%m-01")
    actuals["coverage_scope"] = COVERAGE

    # --- live forecast: 80 rows, horizon dimension confined here ---
    table = build_horizon_table(prefer_db=prefer_db, L_arrivals=art["L_arrivals"])
    _, live = split_train_and_live(table)
    Xlive = live[feats + [config.CATEGORICAL_FEATURE]].copy()
    Xlive[config.CATEGORICAL_FEATURE] = (Xlive[config.CATEGORICAL_FEATURE].astype("category")
                                         .cat.set_categories(art["category_levels"]))
    live = live.assign(predicted_arrivals=np.clip(model.predict(Xlive), 0, None).round(0))

    forecast = pd.DataFrame({
        "source_country_iso3": live["source_country_iso3"],
        "source_country_name": live["source_country_name"],
        "market_segment": live["market_segment"],
        "period": live["target_period"].dt.strftime("%Y-%m-01"),
        "year": live["target_period"].dt.year,
        "month": live["target_period"].dt.month,
        "horizon": live["horizon"],
        "predicted_arrivals": live["predicted_arrivals"],
        "actual_arrivals": np.nan,
        "split_type": "future_forecast",
        "forecast_assumption": f"L_arrivals={art['L_arrivals']} (primary)",
        "coverage_scope": COVERAGE,
    })

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    actuals.to_csv(config.OUTPUT_DIR / "historical_actuals.csv", index=False)
    forecast.to_csv(config.OUTPUT_DIR / "forecast_future_2026.csv", index=False)

    # basic sanity gate
    assert len(forecast) == 80, f"Expected 80 forecast rows, got {len(forecast)}"
    assert forecast["predicted_arrivals"].notna().all(), "Missing predictions"
    assert (forecast["predicted_arrivals"] >= 0).all(), "Negative predictions"
    assert actuals.duplicated(["source_country_iso3", "period"]).sum() == 0, "Duplicate actuals"
    print(f"Wrote historical_actuals.csv ({len(actuals)}) and forecast_future_2026.csv ({len(forecast)}).")
    return actuals, forecast


if __name__ == "__main__":
    generate_outputs()
