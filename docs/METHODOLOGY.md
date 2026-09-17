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
- **Metrics:** MAE and RMSE, per horizon. MAPE avoided (near-zero small-market
  months inflate it).

## 5. Models compared (no more, per lecturer)
- Naive-last, Seasonal-naive (baselines), Ridge + GPR×country, LightGBM.
- **Deployed:** LightGBM (most consistently competitive; Ridge collapses under
  the COVID break). Ridge retained only for interpretable GPR×country
  coefficients.
- **Champion-by-horizon rejected:** inter-model gaps are small and unstable
  across folds/lag assumptions — switching per horizon would fit noise.

## 6. Feature set (locked, 19 + 1 categorical)
Curated from a fuller set; pruning to 18 cost +16–19% MAE at horizon 2, so
`target_month_cos` was restored → 19 features within ~2% of the full set.
Dropped: all 5 MEI indices (stale after availability-capping + low importance),
RON95, east-Malaysia diesel, mom_growth. `source_country_iso3` is the 20th
input (categorical). "19-feature model" and "20 model inputs" both refer to
this same model.

## 7. GPR interpretation (two tools, both non-causal)
- **Ridge GPR×country**, USA as dropped reference → identifiable per-country
  slopes. The pooled main GPR effect is positive, almost certainly a spurious
  co-movement with the post-COVID recovery trend — **not** behavioural.
- **LightGBM + SHAP**, mean |SHAP| of GPR features by country: raw (dominated by
  market size) and **normalized by each market's average arrival volume**
  (noisy/inflated for small-base markets). Both are model-attributed
  contribution, **not causal country sensitivity**.

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
