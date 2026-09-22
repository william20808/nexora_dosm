"""
machine_learning/run_pipeline.py

One command to reproduce the entire ML workstream end to end:
  1. train the final LightGBM  -> artifacts/lightgbm_final.joblib
  2. generate forecasts + actuals -> outputs/historical_actuals.csv, forecast_future_2026.csv
  3. run the backtest             -> outputs/backtest_*.csv, covid_*, L3_vs_L4_*
  4. run explainability          -> outputs/lightgbm_feature_importance.csv, gpr_*, shap_*

Run from the repo root:
    python -m machine_learning.run_pipeline
"""

from .train import train_final_model
from .predict import generate_outputs
from .evaluate import run_all as run_backtest
from .explainability import run_all as run_explain


def main():
    print("[1/4] Training final model ...")
    train_final_model()

    print("[2/4] Generating forecasts and actuals ...")
    generate_outputs()

    print("[3/4] Running backtest ...")
    run_backtest()

    print("[4/4] Running explainability ...")
    run_explain()

    print(
        "\nDone. See machine_learning/outputs/ for all tables and "
        "machine_learning/artifacts/ for the model."
    )


if __name__ == "__main__":
    main()
