-- ==============================================================================
-- DOSM Tourism Datathon: Essential Analytical & Modeling SQL Queries
-- Database: dosm_datathon.db
-- Data Source: monthly_shared_predictors_corrected_mar2017.xlsx
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Inbound Tourism Trend Joined with Macroeconomic & Geopolitical Predictors
-- Evaluates monthly arrivals across all countries against key external macro variables:
-- Brent Crude, local fuel price (RON95), leading economic index, and GPR index.
-- ------------------------------------------------------------------------------
SELECT 
    p.year,
    p.month,
    ROUND(SUM(p.monthly_tourist_arrivals), 0) AS total_tourist_arrivals,
    ROUND(AVG(p.monthly_myr_per_source_currency), 4) AS avg_currency_rate,
    ROUND(m.brent_crude_usd_bbl, 2) AS brent_crude_usd_bbl,
    ROUND(m.ron95_rm_litre_monthly_avg, 2) AS ron95_price_myr,
    ROUND(m.leading_index, 2) AS leading_economic_index,
    ROUND(m.coincident_index, 2) AS coincident_index,
    ROUND(m.gpr_global_index, 2) AS gpr_global_index,
    ROUND(m.gpr_malaysia_index, 4) AS gpr_malaysia_index
FROM imputed_panel_data p
LEFT JOIN imputed_time_series_data m 
  ON p.year = m.year AND p.month = m.month_number
WHERE p.model_row_status = 'Training eligible'
GROUP BY p.year, p.month
ORDER BY p.year, p.month;


-- ------------------------------------------------------------------------------
-- 2. Source Country Inbound Ranking & Overall Market Share
-- Ranks all 20 origin countries by cumulative inbound volume and percentage share.
-- ------------------------------------------------------------------------------
SELECT 
    source_country_iso3,
    source_country_name,
    market_segment,
    source_currency_code,
    ROUND(SUM(monthly_tourist_arrivals), 0) AS cumulative_arrivals,
    ROUND(AVG(monthly_tourist_arrivals), 0) AS avg_monthly_arrivals,
    ROUND(
        SUM(monthly_tourist_arrivals) * 100.0 / (
            SELECT SUM(monthly_tourist_arrivals) 
            FROM imputed_panel_data 
            WHERE model_row_status = 'Training eligible'
        ), 2
    ) AS market_share_pct
FROM imputed_panel_data
WHERE model_row_status = 'Training eligible'
GROUP BY source_country_iso3, source_country_name, market_segment, source_currency_code
ORDER BY cumulative_arrivals DESC;


-- ------------------------------------------------------------------------------
-- 3. Tourism Seasonality Breakdown (Monthly Arrival Distribution)
-- Evaluates calendar month seasonality across all recorded years (months 1-12).
-- Useful for feature engineering (cyclical encoding: sin/cos of month).
-- ------------------------------------------------------------------------------
SELECT 
    month AS calendar_month,
    CASE month
        WHEN 1 THEN 'January'
        WHEN 2 THEN 'February'
        WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'
        WHEN 5 THEN 'May'
        WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'
        WHEN 8 THEN 'August'
        WHEN 9 THEN 'September'
        WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'
        WHEN 12 THEN 'December'
    END AS month_name,
    ROUND(AVG(monthly_tourist_arrivals), 0) AS avg_arrivals_per_country,
    ROUND(SUM(monthly_tourist_arrivals), 0) AS total_arrivals_across_years,
    COUNT(DISTINCT date) AS total_observation_dates
FROM imputed_panel_data
WHERE model_row_status = 'Training eligible'
GROUP BY month
ORDER BY month;


-- ------------------------------------------------------------------------------
-- 4. ASEAN vs Non-ASEAN Regional Segment Comparison Over Time
-- Compares regional tourist flows and growth trends by year.
-- ------------------------------------------------------------------------------
SELECT 
    year,
    market_segment,
    COUNT(DISTINCT source_country_iso3) AS country_count,
    ROUND(SUM(monthly_tourist_arrivals), 0) AS total_arrivals,
    ROUND(AVG(monthly_tourist_arrivals), 0) AS avg_monthly_arrivals,
    ROUND(AVG(monthly_myr_per_source_currency), 4) AS avg_myr_per_currency
FROM imputed_panel_data
WHERE model_row_status = 'Training eligible'
GROUP BY year, market_segment
ORDER BY year, market_segment;


-- ------------------------------------------------------------------------------
-- 5. Foreign Exchange Rate Impact by Country
-- Analyzes how currency strength (MYR per source currency) correlates with arrivals.
-- ------------------------------------------------------------------------------
SELECT 
    source_country_iso3,
    source_country_name,
    source_currency_code,
    year,
    ROUND(AVG(monthly_myr_per_source_currency), 4) AS avg_fx_rate,
    ROUND(SUM(monthly_tourist_arrivals), 0) AS total_annual_arrivals
FROM imputed_panel_data
WHERE model_row_status = 'Training eligible'
GROUP BY source_country_iso3, source_country_name, source_currency_code, year
ORDER BY source_country_iso3, year;


-- ------------------------------------------------------------------------------
-- 6. Machine Learning Dataset Split: Training vs Hold-Out Target
-- Verifies the partition between training eligible rows and evaluation hold-out set.
-- ------------------------------------------------------------------------------
SELECT 
    model_row_status,
    COUNT(*) AS row_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM imputed_panel_data), 2) AS pct_of_dataset,
    MIN(date) AS start_date,
    MAX(date) AS end_date,
    COUNT(DISTINCT source_country_iso3) AS country_count,
    SUM(target_missing_flag) AS missing_target_count
FROM imputed_panel_data
GROUP BY model_row_status;


-- ------------------------------------------------------------------------------
-- 7. Imputation Assessment: Ground Truth vs Imputed Predictors
-- Identifies months where macroeconomic predictors were estimated vs observed.
-- ------------------------------------------------------------------------------
SELECT 
    year,
    month_number,
    month,
    imputation_status,
    imputed_predictor_count,
    gpr_global_index_imputed_flag,
    brent_crude_usd_bbl_imputed_flag,
    leading_index_imputed_flag,
    ron95_rm_litre_monthly_avg,
    brent_crude_usd_bbl
FROM imputed_time_series_data
WHERE any_predictor_imputed_flag = 1
ORDER BY year, month_number;


-- ------------------------------------------------------------------------------
-- 8. Post-Pandemic Tourism Recovery Tracker (2019 Benchmark vs Post-2022)
-- Compares pre-pandemic peak tourism (2019) against recovery years (2023-2026).
-- ------------------------------------------------------------------------------
WITH annual_totals AS (
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
    t2019.source_country_iso3,
    t2019.source_country_name,
    ROUND(t2019.arrivals, 0) AS arrivals_2019_baseline,
    ROUND(t2024.arrivals, 0) AS arrivals_2024,
    ROUND((t2024.arrivals - t2019.arrivals) * 100.0 / t2019.arrivals, 2) AS recovery_pct_vs_2019
FROM (SELECT * FROM annual_totals WHERE year = 2019) t2019
LEFT JOIN (SELECT * FROM annual_totals WHERE year = 2024) t2024
  ON t2019.source_country_iso3 = t2024.source_country_iso3
ORDER BY arrivals_2019_baseline DESC;
