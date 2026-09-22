# Machine Learning Pipeline

Forecasts monthly international tourist arrivals to Malaysia for 20 source
markets, one to four months ahead. All arrival totals in this project cover
only those 20 markets, not all international arrivals to Malaysia.

## Run the pipeline

From the repository root:

```bash
pip install -r requirements.txt
python -m machine_learning.run_pipeline
```

The pipeline reads `data/dosm_datathon.db`, regenerates the CSV files in
`outputs/`, and writes the trained LightGBM model to `artifacts/`. The
configuration and random seed are fixed; different numerical-library builds
may still produce negligible floating-point differences.

Individual stages can also be run directly:

```bash
python -m machine_learning.train
python -m machine_learning.predict
python -m machine_learning.evaluate
python -m machine_learning.explainability
```

## Structure

```text
machine_learning/
├── README.md
├── DATA_DICTIONARY.md
├── config.py
├── data_loader.py
├── feature_engineering.py
├── train.py
├── predict.py
├── evaluate.py
├── explainability.py
├── run_pipeline.py
├── artifacts/
│   └── lightgbm_final.joblib
└── outputs/
    ├── historical_actuals.csv
    ├── forecast_future_2026.csv
    ├── backtest_predictions.csv
    ├── backtest_accuracy_by_horizon.csv
    ├── covid_stress_test_summary.csv
    ├── L3_vs_L4_sensitivity_summary.csv
    ├── lightgbm_feature_importance.csv
    ├── gpr_country_ridge_interaction.csv
    └── shap_gpr_contribution_by_country.csv
```

`DATA_DICTIONARY.md` defines every output column and metric. The committed CSV
files are retained because they are the validated results used by the report
and Power BI dashboard; the model artifact allows the forecast stage to run
without retraining.

## Method

The deployed model is a pooled direct multi-horizon LightGBM. It uses lagged
arrivals, seasonal signals, exchange rates, geopolitical-risk indices, energy
prices, and a country category. Publication lags in `config.py` ensure each
feature represents information that would have been available at forecast
time.

Rolling-origin backtesting compares LightGBM with naive-last,
seasonal-naive, and Ridge baselines using MAE and RMSE. Separate COVID stress
folds and an arrivals-lag sensitivity test assess robustness. LightGBM is the
deployed model based on aggregate primary-backtest MAE, although it is not the
best model at every individual horizon.

## Interpretation guardrails

- Use `historical_actuals.csv` for historical totals. Do not sum rows from a
  table containing multiple forecast horizons.
- Use the backtest outputs for accuracy claims; in-sample fit is not an
  accuracy measure.
- GPR interaction and SHAP results are model associations, not causal effects.
- Treat normalized SHAP ratios cautiously for low-volume source markets.
