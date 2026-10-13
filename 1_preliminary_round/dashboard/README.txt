================================================================================
TEAM NEXORA - DOSM DATATHON 2026
INTERACTIVE DASHBOARD USER GUIDE AND SPECIFICATIONS
================================================================================

PACKAGE CONTENTS
----------------
Dashboard.pdf   Static version of the four dashboard pages
Dashboard.pbix  Interactive Microsoft Power BI dashboard
Data.xlsx       Supporting source, forecast, and model-validation tables
README.txt      Opening instructions, navigation guide, and limitations

1. SOFTWARE NAME AND VERSION
----------------------------
* Software: Microsoft Power BI Desktop (64-bit Windows)
* Version: 2.127.707.0 or later is recommended. The PBIX package records query
  engine version 2.127.707.0.

2. HOW TO OPEN THE DASHBOARD
----------------------------
Step 1: Extract all four files from "Nexora_Datathon2026_Dashboard.zip" into
        the same local folder.
Step 2: Open "Dashboard.pbix" in Microsoft Power BI Desktop.
Step 3: Wait for all four report pages to load:
        - Malaysia Tourism Overview
        - Market Analysis
        - Tourism Drivers
        - Forecast
Step 4: Use the report-page tabs at the bottom to move between pages.
Step 5: If Power BI requests a source path, choose Home > Transform data >
        Data source settings, point the workbook source to "Data.xlsx" in the
        extracted folder, and select Close & Apply.
Step 6: Open "Dashboard.pdf" when only a static view is required.

3. HOW TO NAVIGATE AND INTERACT
-------------------------------
* Slicers: Use Source Country and Market Segment controls where displayed.
* Cross-filtering: Select a bar, line point, or donut segment to filter linked
  visuals on the same page. Select the same item again or click blank canvas
  space to clear the selection.
* Tooltips: Hover over a data point to see its month, market, and measure value.
* Resetting: Clear slicer selections or reopen the report to return to the
  saved default view.

4. DATA.XLSX CONTENTS
---------------------
* Country Panel (Monthly): 2,300 country-month rows for 20 source markets.
* Time Series Macro: Monthly geopolitical-risk, crude-oil, economic, and fuel
  indicators.
* Forecast 2026: Four-month forecasts for June-September 2026.
* Backtest Predictions: Out-of-sample actual and predicted arrivals.
* Backtest Accuracy: MAE and RMSE by model, lag choice, fold set, and horizon.
* COVID Stress Test: Model accuracy during the COVID stress-test folds.
* Lag Sensitivity: Comparison of three-month and four-month arrival lags.
* Feature Importance: LightGBM feature-importance scores.
* GPR Ridge Interaction: Country-level geopolitical-risk interaction effects.
* SHAP GPR Contribution: Country-level normalized GPR contributions.

5. REQUIRED PLUGINS OR ADD-ONS
------------------------------
* None. The report uses standard Power BI visuals only.
* No marketplace visuals, scripts, or external database connection are
  required for normal offline viewing of the saved PBIX.

6. ASSUMPTIONS, LIMITATIONS, AND SPECIAL CONSIDERATIONS
-------------------------------------------------------
* Actual tourist-arrival data run from March 2017 through May 2026.
* The analysis covers 20 modelled source markets. Totals are not an all-Malaysia
  international-arrivals total.
* June-September 2026 values are model forecasts, not published DOSM actuals
  and not official government forecasts.
* Forecast totals for the 20 markets are 2,278,401 (June), 2,287,744 (July),
  2,173,788 (August), and 2,054,893 (September).
* Missing future arrival values in Data.xlsx are intentional because those rows
  represent the forecast horizon.
* Bilateral exchange rates are monthly averages expressed as MYR per unit of
  source-market currency.
* GPR results describe model associations and contributions; they do not prove
  that geopolitical risk causes a change in tourist arrivals.
* The PBIX includes an embedded data cache for offline judging. Data.xlsx is
  included for transparency, reproducibility, and source review.
================================================================================
