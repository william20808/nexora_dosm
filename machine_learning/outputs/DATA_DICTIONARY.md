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
Headline: LightGBM was selected on AGGREGATE MAE pooled across all primary
backtest predictions (15,969 vs Ridge 16,727, Naive-last 17,188, Seasonal-naive
22,702), which is the criterion matching the single-pooled-model design.
Per-horizon MAE (primary, L=4) is split:
  h1  LightGBM 11,817 | Naive-last 12,752 | Ridge 12,117 | Seasonal-naive 23,802
  h2  LightGBM  9,571 | Naive-last  9,671 | Ridge  9,757 | Seasonal-naive 20,404
  h3  LightGBM 21,504 | Naive-last 25,157 | Ridge 24,258 | Seasonal-naive 21,191
  h4  LightGBM 20,983 | Naive-last 21,171 | Ridge 20,775 | Seasonal-naive 25,413
LightGBM is best at h1-h2; Seasonal-naive is marginally best at h3 and Ridge
marginally best at h4 (margins of 100-313 arrivals, inside fold-level noise).
Do NOT claim LightGBM is best at every horizon, and do NOT overstate this as ML
"solving" forecasting — no model beats naive persistence under the COVID break.

## 5. lightgbm_feature_importance.csv
20 rows = the 19 numeric features + source_country_iso3. feature, importance
(relative split-count, unitless).

## 6. gpr_country_ridge_interaction.csv
Ridge with GPR x country interaction, USA as reference (identifiable).

SCHEMA CHANGED — old columns `gpr_interaction_vs_USA` and
`total_standardized_gpr_slope` no longer exist. Current columns:
- source_country_iso3, market_segment
- gpr_interaction_vs_USA_raw: this market's interaction term in RAW feature
  space (0 for USA by construction)
- gpr_slope_raw_per_index_point: full slope, arrivals per 1 GPR index point
- gpr_slope_arrivals_per_1sd_gpr: full slope per 1 standard deviation of GPR —
  USE THIS for cross-market comparison and for any visual

Slopes are recovered in raw space before summing base + interaction, because
the standardized columns have different scales (~0.59x) and cannot be added.
Verified by perturbation (max discrepancy 0.0 across all 20 markets).
16 of 20 markets have a negative slope; SGP, IDN, CHN are positive; THA is
essentially zero (+297 arrivals per 1 SD).
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
- Never claim LightGBM is best at every horizon — it is not (h3, h4 go to other models).
- Never present the h3-h4 advantage without the COVID stress-test caveat.
- Never describe GPR x country or SHAP results as causal country sensitivity.
