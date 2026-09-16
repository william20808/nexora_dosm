-- ==============================================================================
-- DOSM Tourism Datathon 2026: Comprehensive SQL Query Suite
-- Database: dosm_datathon.db (SQLite)
-- Dataset: dataset.xlsx
--
-- Structure:
--   PART 1: DATA VIEWING & AUDITING (Data Engineering Sanity Checks)
--   PART 2: EXPLORATORY DATA ANALYSIS (EDA & Statistical Aggregations)
--   PART 3: FEATURE ENGINEERING (Machine Learning Pipeline Preparation)
-- ==============================================================================


-- ==============================================================================
-- PART 1: DATA VIEWING & AUDITING (Data Engineering Sanity Checks)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1.1 Variable Provenance & Metadata Lookup
-- Inspects variable definitions, source agencies, original APIs, and missing rates.
-- ------------------------------------------------------------------------------
SELECT 
    workbook_sheet,
    variable_code,
    variable_name,
    release_agency,
    source_dataset_or_series,
    measurement_unit,
    original_missing_rate_pct,
    api_or_download_url_used
FROM sources
ORDER BY workbook_sheet, variable_code;


-- ------------------------------------------------------------------------------
-- 1.2 Panel Balance & Temporal Coverage Verification
-- Verifies that all 20 origin countries have identical date counts and date ranges.
-- ------------------------------------------------------------------------------
SELECT 
    source_country_iso3,
    source_country_name,
    market_segment,
    source_currency_code,
    COUNT(*) AS total_daily_rows,
    COUNT(DISTINCT date) AS distinct_dates,
    MIN(date) AS earliest_date,
    MAX(date) AS latest_date,
    COUNT(DISTINCT year || '-' || printf('%02d', month)) AS distinct_year_months
FROM imputed_panel_data
GROUP BY source_country_iso3, source_country_name, market_segment, source_currency_code
ORDER BY market_segment, source_country_iso3;


-- ------------------------------------------------------------------------------
-- 1.3 Imputation Audit: Raw vs. Imputed Time-Series Predictors
-- Compares original un-imputed values with imputed values to inspect where
-- missing values were substituted.
-- ------------------------------------------------------------------------------
SELECT 
    i.year,
    i.month_number,
    i.imputation_status,
    i.imputed_predictor_count,
    -- Brent Crude comparison
    o.brent_crude_usd_bbl AS raw_brent,
    i.brent_crude_usd_bbl AS imputed_brent,
    i.brent_crude_usd_bbl_imputed_flag AS brent_flag,
    -- Leading Index comparison
    o.leading_index AS raw_leading_index,
    i.leading_index AS imputed_leading_index,
    i.leading_index_imputed_flag AS leading_flag,
    -- GPR Index comparison
    o.gpr_global_index AS raw_gpr_global,
    i.gpr_global_index AS imputed_gpr_global,
    i.gpr_global_index_imputed_flag AS gpr_flag
FROM imputed_time_series_data i
LEFT JOIN original_time_series_data o 
  ON i.year = o.year AND i.month_number = o.month_number
WHERE i.any_predictor_imputed_flag = 1
ORDER BY i.year, i.month_number;


-- ------------------------------------------------------------------------------
-- 1.4 Target Availability & Competition Partition Audit
-- Audits rows designated for model training versus hold-out scoring horizon.
-- ------------------------------------------------------------------------------
SELECT 
    model_row_status,
    COUNT(*) AS total_panel_rows,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM imputed_panel_data), 2) AS pct_of_dataset,
    MIN(date) AS min_date,
    MAX(date) AS max_date,
    COUNT(DISTINCT source_country_iso3) AS country_count,
    SUM(target_missing_flag) AS missing_target_rows,
    SUM(monthly_arrivals_available_flag) AS available_target_rows
FROM imputed_panel_data
GROUP BY model_row_status;


-- ------------------------------------------------------------------------------
-- 1.5 Country Reference & Currency Master List
-- Clean lookup table for all origin markets, currencies, and regional classifications.
-- ------------------------------------------------------------------------------
SELECT DISTINCT 
    source_country_iso3,
    source_country_name,
    market_segment,
    source_currency_code
FROM imputed_panel_data
ORDER BY market_segment, source_country_name;



-- ==============================================================================
-- PART 2: EXPLORATORY DATA ANALYSIS (EDA & Statistical Aggregations)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 2.1 Source Market Volume Ranking & Summary Statistics
-- Computes total volume, mean, minimum, maximum, and overall market share.
-- ------------------------------------------------------------------------------
WITH country_monthly AS (
    SELECT 
        source_country_iso3,
        source_country_name,
        market_segment,
        year,
        month,
        monthly_tourist_arrivals
    FROM imputed_panel_data
    WHERE model_row_status = 'Training eligible'
    GROUP BY source_country_iso3, year, month
)
SELECT 
    source_country_iso3,
    source_country_name,
    market_segment,
    ROUND(SUM(monthly_tourist_arrivals), 0) AS cumulative_arrivals,
    ROUND(AVG(monthly_tourist_arrivals), 0) AS avg_monthly_arrivals,
    ROUND(MIN(monthly_tourist_arrivals), 0) AS min_monthly_arrivals,
    ROUND(MAX(monthly_tourist_arrivals), 0) AS max_monthly_arrivals,
    ROUND(
        SUM(monthly_tourist_arrivals) * 100.0 / (
            SELECT SUM(monthly_tourist_arrivals) 
            FROM country_monthly
        ), 2
    ) AS market_share_pct
FROM country_monthly
GROUP BY source_country_iso3, source_country_name, market_segment
ORDER BY cumulative_arrivals DESC;


-- ------------------------------------------------------------------------------
-- 2.2 Seasonality Analysis: Monthly Arrival Distribution Across All Markets
-- Calculates average arrivals and seasonal volume across calendar months (1-12).
-- ------------------------------------------------------------------------------
WITH monthly_totals AS (
    SELECT 
        year,
        month,
        SUM(monthly_tourist_arrivals) AS total_monthly_volume
    FROM imputed_panel_data
    WHERE model_row_status = 'Training eligible'
    GROUP BY year, month
)
SELECT 
    month AS calendar_month,
    CASE month
        WHEN 1 THEN 'Jan' WHEN 2 THEN 'Feb' WHEN 3 THEN 'Mar'
        WHEN 4 THEN 'Apr' WHEN 5 THEN 'May' WHEN 6 THEN 'Jun'
        WHEN 7 THEN 'Jul' WHEN 8 THEN 'Aug' WHEN 9 THEN 'Sep'
        WHEN 10 THEN 'Oct' WHEN 11 THEN 'Nov' WHEN 12 THEN 'Dec'
    END AS month_name,
    COUNT(year) AS years_observed,
    ROUND(AVG(total_monthly_volume), 0) AS avg_arrivals_in_month,
    ROUND(MIN(total_monthly_volume), 0) AS min_arrivals_in_month,
    ROUND(MAX(total_monthly_volume), 0) AS max_arrivals_in_month
FROM monthly_totals
GROUP BY month
ORDER BY month;


-- ------------------------------------------------------------------------------
-- 2.3 Regional Dynamics: ASEAN vs. Non-ASEAN Annual Volume & Share
-- Compares regional tourist flows and proportion over the 10-year period.
-- ------------------------------------------------------------------------------
SELECT 
    year,
    market_segment,
    COUNT(DISTINCT source_country_iso3) AS country_count,
    ROUND(SUM(monthly_tourist_arrivals), 0) AS total_arrivals,
    ROUND(AVG(monthly_tourist_arrivals), 0) AS avg_monthly_per_country,
    ROUND(AVG(monthly_myr_per_source_currency), 4) AS avg_fx_rate
FROM imputed_panel_data
WHERE model_row_status = 'Training eligible'
GROUP BY year, market_segment
ORDER BY year, market_segment;


-- ------------------------------------------------------------------------------
-- 2.4 Currency Exchange Rate Volatility & Trajectory by Origin Market
-- Analyzes bilateral exchange rate levels, minimum, maximum, and annual spread.
-- ------------------------------------------------------------------------------
SELECT 
    source_country_iso3,
    source_country_name,
    source_currency_code,
    year,
    ROUND(AVG(monthly_myr_per_source_currency), 4) AS avg_fx_rate,
    ROUND(MIN(monthly_myr_per_source_currency), 4) AS min_fx_rate,
    ROUND(MAX(monthly_myr_per_source_currency), 4) AS max_fx_rate,
    ROUND(MAX(monthly_myr_per_source_currency) - MIN(monthly_myr_per_source_currency), 4) AS annual_fx_spread
FROM imputed_panel_data
GROUP BY source_country_iso3, source_country_name, source_currency_code, year
ORDER BY source_country_iso3, year;


-- ------------------------------------------------------------------------------
-- 2.5 Macroeconomic Time Series Overview
-- Consolidated monthly view of fuel prices, economic indices, and GPR scores.
-- ------------------------------------------------------------------------------
SELECT 
    year,
    month_number,
    month,
    ROUND(brent_crude_usd_bbl, 2) AS brent_usd,
    ROUND(ron95_rm_litre_monthly_avg, 2) AS ron95_rm,
    ROUND(ron97_rm_litre_monthly_avg, 2) AS ron97_rm,
    ROUND(diesel_peninsular_rm_litre_monthly_avg, 2) AS diesel_peninsular_rm,
    ROUND(leading_index, 2) AS leading_index,
    ROUND(coincident_index, 2) AS coincident_index,
    ROUND(lagging_index, 2) AS lagging_index,
    ROUND(gpr_global_index, 2) AS gpr_global,
    ROUND(gpr_malaysia_index, 4) AS gpr_malaysia
FROM imputed_time_series_data
ORDER BY year, month_number;


-- ------------------------------------------------------------------------------
-- 2.6 Historical Benchmark: Pre-Pandemic (2019) vs Post-Pandemic Recovery
-- Compares pre-pandemic baseline (2019) arrivals with recovery volumes.
-- ------------------------------------------------------------------------------
WITH annual_country_arrivals AS (
    SELECT 
        source_country_iso3,
        source_country_name,
        year,
        SUM(monthly_tourist_arrivals) AS arrivals
    FROM imputed_panel_data
    WHERE year IN (2019, 2023, 2024, 2025) AND model_row_status = 'Training eligible'
    GROUP BY source_country_iso3, source_country_name, year
)
SELECT 
    y2019.source_country_iso3,
    y2019.source_country_name,
    ROUND(y2019.arrivals, 0) AS arrivals_2019_baseline,
    ROUND(y2023.arrivals, 0) AS arrivals_2023,
    ROUND(y2024.arrivals, 0) AS arrivals_2024,
    ROUND((y2024.arrivals - y2019.arrivals) * 100.0 / y2019.arrivals, 2) AS recovery_pct_2024_vs_2019
FROM (SELECT * FROM annual_country_arrivals WHERE year = 2019) y2019
LEFT JOIN (SELECT * FROM annual_country_arrivals WHERE year = 2023) y2023 
  ON y2019.source_country_iso3 = y2023.source_country_iso3
LEFT JOIN (SELECT * FROM annual_country_arrivals WHERE year = 2024) y2024 
  ON y2019.source_country_iso3 = y2024.source_country_iso3
ORDER BY arrivals_2019_baseline DESC;



-- ==============================================================================
-- PART 3: FEATURE ENGINEERING (Machine Learning Pipeline Preparation)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 3.1 Time-Series Lag Generation (Lags: t-1, t-2, t-3, t-6, t-12)
-- Generates autoregressive lag features per country using SQL window functions.
-- Lag 12 represents the same-month seasonal baseline from the previous year.
-- ------------------------------------------------------------------------------
WITH monthly_series AS (
    SELECT 
        source_country_iso3,
        source_country_name,
        market_segment,
        year,
        month,
        monthly_tourist_arrivals,
        monthly_myr_per_source_currency,
        model_row_status
    FROM imputed_panel_data
    GROUP BY source_country_iso3, year, month
)
SELECT 
    source_country_iso3,
    source_country_name,
    market_segment,
    year,
    month,
    monthly_tourist_arrivals AS target_arrivals,
    LAG(monthly_tourist_arrivals, 1) OVER w AS arrivals_lag_1m,
    LAG(monthly_tourist_arrivals, 2) OVER w AS arrivals_lag_2m,
    LAG(monthly_tourist_arrivals, 3) OVER w AS arrivals_lag_3m,
    LAG(monthly_tourist_arrivals, 6) OVER w AS arrivals_lag_6m,
    LAG(monthly_tourist_arrivals, 12) OVER w AS arrivals_lag_12m,
    LAG(monthly_myr_per_source_currency, 1) OVER w AS fx_rate_lag_1m
FROM monthly_series
WINDOW w AS (PARTITION BY source_country_iso3 ORDER BY year, month)
ORDER BY source_country_iso3, year, month;


-- ------------------------------------------------------------------------------
-- 3.2 Rolling Window Statistics (3-Month & 6-Month Moving Averages & Momentum)
-- Calculates trailing moving averages and momentum ratios (current vs trailing).
-- ------------------------------------------------------------------------------
WITH monthly_series AS (
    SELECT 
        source_country_iso3,
        source_country_name,
        year,
        month,
        monthly_tourist_arrivals
    FROM imputed_panel_data
    GROUP BY source_country_iso3, year, month
)
SELECT 
    source_country_iso3,
    year,
    month,
    monthly_tourist_arrivals,
    ROUND(AVG(monthly_tourist_arrivals) OVER (
        PARTITION BY source_country_iso3 
        ORDER BY year, month 
        ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
    ), 1) AS rolling_mean_prev_3m,
    ROUND(AVG(monthly_tourist_arrivals) OVER (
        PARTITION BY source_country_iso3 
        ORDER BY year, month 
        ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING
    ), 1) AS rolling_mean_prev_6m,
    ROUND(
        LAG(monthly_tourist_arrivals, 1) OVER (PARTITION BY source_country_iso3 ORDER BY year, month) /
        NULLIF(AVG(monthly_tourist_arrivals) OVER (
            PARTITION BY source_country_iso3 
            ORDER BY year, month 
            ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
        ), 0), 4
    ) AS momentum_ratio_3m
FROM monthly_series
ORDER BY source_country_iso3, year, month;


-- ------------------------------------------------------------------------------
-- 3.3 Growth Rate Indicators: MoM and YoY Relative Change
-- Calculates Month-over-Month (% MoM) and Year-over-Year (% YoY) growth rates.
-- ------------------------------------------------------------------------------
WITH monthly_series AS (
    SELECT 
        source_country_iso3,
        year,
        month,
        monthly_tourist_arrivals
    FROM imputed_panel_data
    GROUP BY source_country_iso3, year, month
)
SELECT 
    source_country_iso3,
    year,
    month,
    monthly_tourist_arrivals,
    ROUND(
        (monthly_tourist_arrivals - LAG(monthly_tourist_arrivals, 1) OVER w) * 100.0 /
        NULLIF(LAG(monthly_tourist_arrivals, 1) OVER w, 0), 2
    ) AS mom_growth_pct,
    ROUND(
        (monthly_tourist_arrivals - LAG(monthly_tourist_arrivals, 12) OVER w) * 100.0 /
        NULLIF(LAG(monthly_tourist_arrivals, 12) OVER w, 0), 2
    ) AS yoy_growth_pct
FROM monthly_series
WINDOW w AS (PARTITION BY source_country_iso3 ORDER BY year, month)
ORDER BY source_country_iso3, year, month;


-- ------------------------------------------------------------------------------
-- 3.4 Cross-Variable Interaction & Ratios (Macro x Currency)
-- Computes interaction features between foreign exchange rates, fuel costs,
-- and economic leading indicators.
-- ------------------------------------------------------------------------------
SELECT 
    p.year,
    p.month,
    p.source_country_iso3,
    p.source_country_name,
    p.monthly_tourist_arrivals,
    p.monthly_myr_per_source_currency,
    m.brent_crude_usd_bbl,
    m.ron95_rm_litre_monthly_avg,
    m.leading_index,
    m.gpr_global_index,
    -- Interaction: Currency Strength x Global Oil Price
    ROUND(p.monthly_myr_per_source_currency * m.brent_crude_usd_bbl, 4) AS fx_x_brent,
    -- Ratio: Domestic Fuel Price to Exchange Rate
    ROUND(m.ron95_rm_litre_monthly_avg / NULLIF(p.monthly_myr_per_source_currency, 0), 4) AS fuel_to_fx_ratio,
    -- Index Ratio: Leading Index to GPR Global
    ROUND(m.leading_index / NULLIF(m.gpr_global_index, 0), 4) AS leading_to_gpr_ratio
FROM (
    SELECT source_country_iso3, source_country_name, year, month, monthly_tourist_arrivals, monthly_myr_per_source_currency
    FROM imputed_panel_data
    GROUP BY source_country_iso3, year, month
) p
LEFT JOIN imputed_time_series_data m 
  ON p.year = m.year AND p.month = m.month_number
ORDER BY p.source_country_iso3, p.year, p.month;


-- ------------------------------------------------------------------------------
-- 3.5 Master Training Feature Matrix (Export-Ready for Machine Learning)
-- Merges monthly tourist arrivals with lags, rolling statistics, macroeconomic
-- variables, fuel prices, and exchange rates.
-- Filters strictly to: model_row_status = 'Training eligible'.
-- ------------------------------------------------------------------------------
WITH panel_monthly AS (
    SELECT 
        source_country_iso3,
        source_country_name,
        market_segment,
        source_currency_code,
        year,
        month,
        monthly_tourist_arrivals,
        monthly_myr_per_source_currency,
        model_row_status
    FROM imputed_panel_data
    GROUP BY source_country_iso3, year, month
),
lagged_features AS (
    SELECT 
        source_country_iso3,
        year,
        month,
        monthly_tourist_arrivals AS target_arrivals,
        LAG(monthly_tourist_arrivals, 1) OVER w AS lag_1m,
        LAG(monthly_tourist_arrivals, 2) OVER w AS lag_2m,
        LAG(monthly_tourist_arrivals, 3) OVER w AS lag_3m,
        LAG(monthly_tourist_arrivals, 12) OVER w AS lag_12m,
        ROUND(AVG(monthly_tourist_arrivals) OVER (
            PARTITION BY source_country_iso3 
            ORDER BY year, month 
            ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
        ), 1) AS rolling_mean_3m,
        ROUND(AVG(monthly_tourist_arrivals) OVER (
            PARTITION BY source_country_iso3 
            ORDER BY year, month 
            ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING
        ), 1) AS rolling_mean_6m
    FROM panel_monthly
    WINDOW w AS (PARTITION BY source_country_iso3 ORDER BY year, month)
)
SELECT 
    p.year,
    p.month,
    p.source_country_iso3,
    p.source_country_name,
    p.market_segment,
    p.source_currency_code,
    -- Target Variable
    lf.target_arrivals,
    -- Autoregressive & Rolling Features
    lf.lag_1m,
    lf.lag_2m,
    lf.lag_3m,
    lf.lag_12m,
    lf.rolling_mean_3m,
    lf.rolling_mean_6m,
    -- Foreign Exchange Features
    p.monthly_myr_per_source_currency,
    -- Macroeconomic Predictors
    m.brent_crude_usd_bbl,
    m.ron95_rm_litre_monthly_avg,
    m.ron97_rm_litre_monthly_avg,
    m.diesel_peninsular_rm_litre_monthly_avg,
    m.diesel_east_malaysia_rm_litre_monthly_avg,
    m.leading_index,
    m.coincident_index,
    m.lagging_index,
    m.leading_diffusion_index,
    m.coincident_diffusion_index,
    m.gpr_global_index,
    m.gpr_malaysia_index,
    -- Temporal Encodings
    CASE WHEN p.market_segment = 'ASEAN' THEN 1 ELSE 0 END AS is_asean
FROM panel_monthly p
JOIN lagged_features lf 
  ON p.source_country_iso3 = lf.source_country_iso3 
 AND p.year = lf.year 
 AND p.month = lf.month
LEFT JOIN imputed_time_series_data m 
  ON p.year = m.year 
 AND p.month = m.month_number
WHERE p.model_row_status = 'Training eligible'
ORDER BY p.source_country_iso3, p.year, p.month;


-- ------------------------------------------------------------------------------
-- 3.6 Master Hold-Out Feature Matrix (Scoring Horizon for Model Predictions)
-- Extracts the exact feature structure for the hold-out competition evaluation
-- period (model_row_status = 'Hold out - target not published').
-- ------------------------------------------------------------------------------
WITH panel_monthly AS (
    SELECT 
        source_country_iso3,
        source_country_name,
        market_segment,
        source_currency_code,
        year,
        month,
        monthly_tourist_arrivals,
        monthly_myr_per_source_currency,
        model_row_status
    FROM imputed_panel_data
    GROUP BY source_country_iso3, year, month
),
lagged_features AS (
    SELECT 
        source_country_iso3,
        year,
        month,
        monthly_tourist_arrivals AS target_arrivals,
        LAG(monthly_tourist_arrivals, 1) OVER w AS lag_1m,
        LAG(monthly_tourist_arrivals, 2) OVER w AS lag_2m,
        LAG(monthly_tourist_arrivals, 3) OVER w AS lag_3m,
        LAG(monthly_tourist_arrivals, 12) OVER w AS lag_12m,
        ROUND(AVG(monthly_tourist_arrivals) OVER (
            PARTITION BY source_country_iso3 
            ORDER BY year, month 
            ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
        ), 1) AS rolling_mean_3m,
        ROUND(AVG(monthly_tourist_arrivals) OVER (
            PARTITION BY source_country_iso3 
            ORDER BY year, month 
            ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING
        ), 1) AS rolling_mean_6m
    FROM panel_monthly
    WINDOW w AS (PARTITION BY source_country_iso3 ORDER BY year, month)
)
SELECT 
    p.year,
    p.month,
    p.source_country_iso3,
    p.source_country_name,
    p.market_segment,
    p.source_currency_code,
    -- Target is null in hold-out
    lf.target_arrivals,
    -- Autoregressive & Rolling Features
    lf.lag_1m,
    lf.lag_2m,
    lf.lag_3m,
    lf.lag_12m,
    lf.rolling_mean_3m,
    lf.rolling_mean_6m,
    -- Foreign Exchange Features
    p.monthly_myr_per_source_currency,
    -- Macroeconomic Predictors
    m.brent_crude_usd_bbl,
    m.ron95_rm_litre_monthly_avg,
    m.ron97_rm_litre_monthly_avg,
    m.diesel_peninsular_rm_litre_monthly_avg,
    m.diesel_east_malaysia_rm_litre_monthly_avg,
    m.leading_index,
    m.coincident_index,
    m.lagging_index,
    m.leading_diffusion_index,
    m.coincident_diffusion_index,
    m.gpr_global_index,
    m.gpr_malaysia_index,
    -- Segment Flag
    CASE WHEN p.market_segment = 'ASEAN' THEN 1 ELSE 0 END AS is_asean
FROM panel_monthly p
JOIN lagged_features lf 
  ON p.source_country_iso3 = lf.source_country_iso3 
 AND p.year = lf.year 
 AND p.month = lf.month
LEFT JOIN imputed_time_series_data m 
  ON p.year = m.year 
 AND p.month = m.month_number
WHERE p.model_row_status = 'Hold out - target not published'
ORDER BY p.source_country_iso3, p.year, p.month;
