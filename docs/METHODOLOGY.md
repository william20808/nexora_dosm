# ML Methodology — DOSM Datathon 2026 (Nexora)

This documents every substantive decision behind the ML workstream so a
teammate, lecturer, or judge can follow and challenge the reasoning. It is the
narrative companion to the code in `machine_learning/`.

## 1. Problem framing
- **Task:** per-country monthly tourist-arrivals forecasting for 20 source
  markets, 1–4 months ahead. Chosen (over a Malaysia-total model) because the
  research question is how different source markets respond to geopolitical /
  economic conditions.
- **Unit of analysis:** country-month. The raw panel stores one row per country
  per day, but monthly measures repeat across all days of a month → collapsed to
  20 × 115 = 2,300 country-months (integrity-asserted in code).
- **Live target:** June–September 2026 arrivals are unpublished (80 country-
  months) — the genuine forecast deliverable, never used in evaluation.

## 2. Design: pooled, direct, multi-horizon
- **Pooled** across all countries + horizons (one model). With ~111 months per
  country, per-country or per-horizon models would starve of data; pooling
  borrows strength across series (the M4/M5 global-model rationale).
- **Direct** (horizon 1–4 predicted from the origin with `horizon` as a
  feature), not recursive — avoids feeding predictions back as inputs and the
  resulting error propagation.
- **Per-horizon reporting** of accuracy, not a single pooled number.

## 3. Information set & availability (the core correctness issue)
Each simulated forecast origin may only use data actually published by then.
- **Arrivals features** (lags, rolling means, growth, seasonal-naive) are
  anchored at the origin — no future target leaks in.
- **Exogenous features** (GPR, Brent, fuel, FX, MEI) are sourced from the
  freshest month available at the simulated present (= origin + arrivals lag),
  using per-variable publication lags. This replaces an arbitrary fixed "gap".
- **Publication lags** (see `config.VARIABLE_LAGS`):
  - MEI (leading/coincident/lagging + diffusion): ~2 months — **verified** from
    DOSM release archives (reference month M released ~20–25th of M+2).
  - GPR (global, Malaysia), Brent: ~1 month — metadata-supported.
  - FX, fuel: ~0 — market/administrative data (BNM daily rates, MOF weekly).
  - Tourist arrivals: assumed 4 months — **not verified** (no public release
    archive found); tested at 3 and 4 as a sensitivity.
- Report wording: *"Features were aligned using documented publication schedules
  where available and conservative lag assumptions where exact release timing
  could not be verified."*

## 4. Backtesting
- **Rolling-origin**, 5 primary (stable-period) folds + 5 COVID stress folds,
  kept separate. COVID retained, not deleted, and reported as a stress test.
- **No-leakage rule (row-level):** a training row is used only if its target
  month was published by the validation origin — not merely if its origin was
  earlier. This closes the horizon-overlap leak that a fixed origin-gap missed.
- **Training-eligibility parity (not a leakage control):** backtest folds apply
  the SAME eligibility rule as final training — rows need a full 12-month
  arrivals history. Note this is distinct from the no-future-information
  controls above: those cold-start rows contained only past and contemporaneous
  data and were genuinely available at every origin, so their earlier inclusion
  was a **backtest-deployment training-eligibility mismatch**, not leakage. It
  was material nonetheless (12-17% of primary-fold and up to 35% of stress-fold
  training rows), because it meant the backtest measured a more data-rich
  procedure than the one actually deployed.
- **Metrics:** MAE and RMSE, per horizon. MAPE avoided (near-zero small-market
  months inflate it).

## 5. Models compared (no more, per lecturer)
- Naive-last, Seasonal-naive (baselines), Ridge + GPR×country, LightGBM.
- **Deployed:** LightGBM, selected on **aggregate MAE pooled across all primary
  backtest predictions** (15,969 vs Ridge 16,727, Naive-last 17,188,
  Seasonal-naive 22,702) and aggregate RMSE (36,043, also lowest). This is the
  criterion that matches the deployed design: one pooled model makes all 80
  forecasts, so total error across all predictions is what matters.
- **The choice is defensible, not decisive.** On rank-based criteria Ridge is
  ahead (7 of 20 fold x horizon cell wins vs LightGBM's 4; mean rank 2.15 vs
  2.30), and LightGBM has the worst single-cell MAE (38,329 vs Ridge 33,129).
  Per-horizon MAE is split: LightGBM best at h1-h2, Seasonal-naive marginally
  best at h3 (21,191 vs 21,504), Ridge marginally best at h4 (20,775 vs 20,983).
  Report LightGBM as competitive everywhere, not as clearly superior.
- **Champion-by-horizon rejected:** the h2-h4 margins are 100-313 arrivals,
  well inside fold-level noise across only five folds — switching per horizon
  would fit noise.

## 6. Feature set (locked, 19 + 1 categorical)
Curated from a fuller set; pruning to 18 cost +16–19% MAE at horizon 2, so
`target_month_cos` was restored → 19 features within ~2% of the full set.
Dropped: all 5 MEI indices (stale after availability-capping + low importance),
RON95, east-Malaysia diesel, mom_growth. `source_country_iso3` is the 20th
input (categorical). "19-feature model" and "20 model inputs" both refer to
this same model.

## 7. GPR interpretation (two tools, both non-causal)

**Three distinct quantities — do not conflate them.** They genuinely differ in
sign and magnitude, and an earlier draft of this document conflated them:

| Quantity | Value | What it is |
|---|---|---|
| Raw pooled correlation, GPR vs arrivals | **+0.079** | Unadjusted association across all country-months. Weakly positive. |
| Within-country (demeaned) correlation | **+0.134** | Removes fixed differences in market size. Still weakly positive. |
| **Ridge GPR slope (controlled)** | **−2,084** arrivals per 1 SD of GPR (USA reference) | Association **after** controlling for arrivals history, seasonality, FX, oil and the other features. **Negative.** |

The raw association is weakly **positive** while the controlled slope is
**negative**, and **16 of 20** country slopes are negative (SGP, IDN, CHN are
the positive outliers; THA sits essentially at zero, +297). This reversal is not
a contradiction — it is what controlling for confounders does. The most likely
driver is shared time trend: over the sample, GPR is strongly trending (corr
with time **+0.54**) while arrivals recovered post-COVID, so an uncontrolled
comparison mixes the trend in; the most likely explanation is that the
lag/seasonality features absorb that trend, leaving a negative partial
association.

**Coefficient recovery (important).** StandardScaler scales each column by its
own SD, and the interaction columns `gpr_x_<country>` have ~0.59x the SD of the
base `gpr_global_index` column. Standardized coefficients are therefore in
different units and must NOT be summed directly. Slopes are recovered in raw
feature space (coef_raw = coef_std / scale) and then summed, and reported per
1 SD of GPR for cross-market comparability. This was verified independently by
perturbation: raising GPR by exactly 1 SD with all other inputs held fixed
reproduces each reported slope with max discrepancy 0.0 across all 20 markets.

**Correction note:** earlier versions of this document (a) described the main GPR
effect as *positive*, attributing it to "GPR falling as arrivals recovered" —
both halves wrong, since the controlled slope is negative and GPR *rose*; and
(b) reported 17 of 20 negative slopes from an invalid summation of differently
scaled standardized coefficients. The corrected figure is 16 of 20.

**The two tools:**
- **Ridge GPR×country**, USA as dropped reference → identifiable per-country
  slopes (`gpr_country_ridge_interaction.csv`). Read as *controlled partial
  associations*, not behavioural responses.
- **LightGBM + SHAP**, mean |SHAP| of GPR features by country: raw (dominated by
  market size) and **normalized by each market's average arrival volume**
  (noisy/inflated for small-base markets). SHAP magnitude is unsigned — it
  measures *how much* the model leans on GPR, not *in which direction*.

**Neither is causal.** Both are single-model, associational attributions from
observational data with no identification strategy. Do not claim GPR *causes*
differential arrivals responses, or that any country is *causally* more
GPR-sensitive.

## 8. Reproducibility
`python -m machine_learning.run_pipeline` regenerates the model and every output
from `data/dosm_datathon.db` with a fixed seed. Verified to reproduce the
finalized 80 forecasts exactly (0 difference) from a clean repo clone.

## 9. Known limitations to disclose
- Arrivals publication lag is assumed, not verified.
- Aug–Sep 2026 exogenous inputs are partly provisional/imputed, so live h3–h4
  reliability is below what backtest metrics on fully-resolved history imply.
- FX has no source-fill flag in the workbook (observed-vs-imputed not auditable).
- Forecasts cover 20 markets only, not all-Malaysia arrivals.
- **Conservative exogenous treatment is a deliberate simplification.** Three
  choices trade a little potential accuracy for defensibility, and each could be
  revisited with more time: (a) MEI lag is encoded as 3 months rather than the
  verified ~2, to stay safe at month boundaries; (b) all 5 MEI indices were
  ultimately dropped from the final feature set, so Malaysia's official
  leading/coincident indicators contribute nothing to the forecast — a real
  information loss, accepted because availability-capping left them stale at the
  horizons where they would have mattered; (c) exogenous predictors enter as
  single-month levels, with no distributed lags, differences or interactions
  beyond GPR×country. A richer exogenous specification is the most obvious
  avenue for future improvement.
