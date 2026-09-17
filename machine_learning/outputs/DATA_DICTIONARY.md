# ML Output Data Dictionary — DOSM Datathon 2026

Model: pooled direct multi-horizon **LightGBM**, forecasting
`monthly_tourist_arrivals` per source country, 1–4 months ahead.
**Model inputs = 20 total: 19 numeric/engineered features + 1 categorical
input (`source_country_iso3`).** Both descriptions refer to the same model.

Primary forecast uses an arrivals publication-lag assumption of **4 months**
(`L_arrivals = 4`); a 3-month variant exists only in the sensitivity file.

**Coverage scope — state this on every arrivals visual:** all figures cover the
**20 modelled source markets only** (a subset of Tourism Malaysia's Top-45
arrivals report). They are **NOT Malaysia's total tourist arrivals from all
countries.** Any monthly total in a visual must be labelled e.g. "Total across
20 modelled markets," never "Malaysia total arrivals."

**Report wording for lags (use verbatim):** *"Features were aligned using
documented publication schedules where available and conservative lag
assumptions where exact release timing could not be verified."*

---

## Why the tables are split (read first)
A single combined table caused **double-counting**: the same historical
country-month appears once per horizon (up to 4x), so summing arrivals over it
inflated real figures up to 4x. The structure below prevents that by giving each
question its own table, with the `horizon` dimension confined to forecast/
backtest tables only.

| To build this visual... | Use this table | Never use |
|---|---|---|
| Historical arrivals trend / totals / seasonality | historical_actuals.csv | the forecast or backtest tables |
| The June-Sept 2026 forecast | forecast_future_2026.csv | - |
| "How accurate is the model?" | backtest_accuracy_by_horizon.csv (metrics) or backtest_predictions.csv (points) | historical_actuals joined to anything |

---

## 1. historical_actuals.csv — source of truth for all historical visuals
**One row per (country, month). No `horizon` column** — cannot double-count.
2,220 rows (20 markets x 111 months).

- source_country_iso3, source_country_name, market_segment: identifiers
- period, year, month: the month (YYYY-MM-01)
- actual_arrivals: real published arrivals
- coverage_scope: reminder text that this is 20 markets, not all-Malaysia

## 2. forecast_future_2026.csv — the 80 forecasts (ONLY table with future rows)
80 rows = 20 markets x Jun-Sep 2026. `horizon` (1-4) lives here.

- identifiers, period, year, month: as above
- horizon: 1-4 months ahead of the May-2026 origin (June=1 ... Sept=4)
- predicted_arrivals: model forecast
- actual_arrivals: blank — unpublished
- split_type: future_forecast
- forecast_assumption: L_arrivals=4 (primary)
- coverage_scope: 20-market reminder

## 3. backtest_predictions.csv — out-of-sample actual-vs-predicted points
The ONLY table whose predictions are genuinely out-of-sample (walk-forward, 5
primary folds). Use for the "did the model track reality?" visual. 400 rows.

- identifiers, period, horizon: as above
- actual_arrivals, predicted_arrivals: both known (historical months)
- fold_origin: which backtest origin produced this prediction
- split_type: backtest_out_of_sample

**Note:** there is deliberately no in-sample "historical_fitted" table any more —
in-sample fit overstates skill and had no legitimate dashboard use.

## 4. backtest_accuracy_by_horizon.csv — the accuracy metrics
MAE/RMSE by L_arrivals x fold_set (primary / stress_covid) x horizon x model.
**This is the source for any accuracy claim.**
Headline: LightGBM is the most consistently competitive model, but only modestly
ahead of simple baselines at SHORT horizons (h1: 12,653 vs naive 12,752 — within
1%). At h3-h4 the margin is real: LightGBM 19,380 vs naive-last 25,157 and
seasonal-naive 21,191 at h3, and better on RMSE at every horizon.
Do NOT overstate this as ML "solving" forecasting — h1-h2 is near-tied with a
trivial baseline, and no model beats naive persistence under the COVID break.

## 5. lightgbm_feature_importance.csv
20 rows = the 19 numeric features + source_country_iso3. feature, importance
(relative split-count, unitless).

## 6. gpr_country_ridge_interaction.csv
Ridge with GPR x country interaction, USA as reference (identifiable).
gpr_interaction_vs_USA, total_standardized_gpr_slope.
**Caveat (must accompany any use):** the pooled GPR effect is likely confounded
with the post-COVID recovery trend; not causal, not verified behaviour.

## 7. shap_gpr_contribution_by_country.csv
Mean |SHAP| of GPR features by country: raw, plus normalized by each market's
average arrival volume (*_normalized_pct).
**Caveats:** raw contribution tracks market size; the normalized ratios are
inflated and noisy for small-base markets (e.g. Nepal, Myanmar, Pakistan) and
should not be read as precise sensitivity. Model-attributed contribution, NOT
causal.

## 8. covid_stress_test_summary.csv
Stress-fold subset of table 4. Under the COVID structural break no model
reliably beats naive persistence.

## 9. L3_vs_L4_sensitivity_summary.csv
LightGBM / Naive / Seasonal MAE under both lag assumptions (primary folds).
Shows the model-selection conclusion is stable to the lag assumption.

---

## Guardrails (do not violate in report or dashboard)
- Never sum actual_arrivals from a table containing a horizon column.
- Never label any total as "Malaysia total arrivals" — it is 20 markets.
- Never present in-sample fit as forecasting accuracy — use the backtest tables.
- Never say lags are "verified" — use the approved wording above.
- Never claim ML dominates at SHORT horizons (h1-h2 is near-tied with naive-last).
- Never present the h3-h4 advantage without the COVID stress-test caveat.
- Never describe GPR x country or SHAP results as causal country sensitivity.
