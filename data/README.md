# 🗄️ Datathon Data Catalog & Variable Dictionary

**Team**: Nexora  
**Competition**: Department of Statistics Malaysia (DOSM) Datathon 2026  
**Primary Assets**: `dosm_datathon.db` (SQLite) & `excel data/final_deliveries_dataset.xlsx` (Excel)

---

## 📌 Data Overview

This directory houses the comprehensive analytical dataset for Team **Nexora**, integrating:
1. **International Country Panel Data**: Monthly horizon from **March 2017 to September 2026** tracking international tourist arrivals across **20 key source markets** alongside bilateral exchange rates and competition hold-out evaluation splits.
2. **National Macroeconomic Time Series**: Monthly indicators spanning energy prices (Brent Crude), retail fuel prices (RON95, RON97, Diesel), Malaysian economic leading/coincident/lagging indices, and global/domestic Geopolitical Risk (GPR) indices.
3. **State-Level Tourism & Hospitality Panel**: Annual panel spanning **2017 to 2025** across **16 Malaysian states and federal territories**, capturing hotel occupancy rates, domestic vs. international hotel guests, and domestic visitor volumes.
4. **Authoritative Variable Provenance Catalog**: Comprehensive metadata mapping 63 variables to custodian agencies, APIs, publications, units, and missingness audit metrics.

```text
data/
├── README.md                 # Data catalog, schema definitions & variable dictionary
├── dosm_datathon.db          # SQLite relational database containing 6 indexed tables & 3 views
├── schema.sql                # Table definitions (DDL), indexing scripts & views
├── queries.sql               # 20 analytical, auditing, and feature engineering SQL queries
└── excel data/
    └── final_deliveries_dataset.xlsx # Master Excel workbook (6 sheets including Sources)
```

---

## 📊 Database Tables Summary

| Table Name | Source Sheet | Rows | Columns | Description |
| :--- | :--- | :---: | :---: | :--- |
| **`imputed_panel_data`** | Imputed Country Panel Data | **69,040** | **12** | Master panel table of monthly tourist arrivals by country, bilateral FX rates, and model split tags. |
| **`original_panel_data`** | Original Country Panel Data | **69,040** | **10** | Un-imputed ground truth monthly country panel observations. |
| **`imputed_time_series_data`** | Imputed Time Series Data | **115** | **37** | Monthly external macroeconomic, energy, and geopolitical predictors with imputed gaps. |
| **`original_time_series_data`** | Original Time Series Data | **115** | **26** | Un-imputed monthly macroeconomic and geopolitical time series. |
| **`hotel_state_annual_panel_data`** | Hotel State Annual Panel Data | **144** | **14** | Annual state-level hotel occupancy rates, guest headcounts (domestic & foreign), and domestic visitor volumes. |
| **`sources`** | Sources | **63** | **17** | Authoritative data dictionary mapping every variable code across all sheets to official sources and APIs. |

> [!NOTE]
> For convenience and backwards compatibility, the database provides views:
> - `imputed_country_panel_data` → alias for `imputed_panel_data`
> - `original_country_panel_data` → alias for `original_panel_data`
> - `hotel_state_panel_data` → alias for `hotel_state_annual_panel_data`

---

## 📋 Country Panel Data Variables (`imputed_panel_data` & `original_panel_data`)

Each observation represents a monthly record for a specific international origin market:

| Variable Name | Data Type | Description & Meaning |
| :--- | :---: | :--- |
| **`date`** | `TEXT` | Calendar observation date in `YYYY-MM-DD` format (first day of each month from 2017-03-01 to 2026-09-01). |
| **`source_country_iso3`** | `TEXT` | 3-letter ISO 3166-1 alpha-3 code identifying the origin market (e.g., `SGP`, `IDN`, `CHN`, `AUS`). |
| **`source_country_name`** | `TEXT` | Full English name of the source market (e.g., Singapore, Indonesia, China, Australia). |
| **`source_currency_code`** | `TEXT` | 3-letter ISO 4217 currency code of the source market (e.g., `SGD`, `IDR`, `CNY`, `AUD`, `USD`). |
| **`market_segment`** | `TEXT` | Regional geopolitical classification of the origin market: `ASEAN` (7 countries) or `Non-ASEAN` (13 countries). |
| **`year`** | `INTEGER` | Calendar year of the observation (2017 to 2026). |
| **`month`** | `INTEGER` | Calendar month of the observation (1 to 12). |
| **`monthly_tourist_arrivals`** | `REAL` | Total count of international tourist arrivals entering Malaysia from the origin country during the month (sourced from Tourism Malaysia / Immigration Department). |
| **`monthly_arrivals_available_flag`** | `INTEGER` | Binary flag (`1` = arrival figure is published and available; `0` = unpublished). |
| **`monthly_myr_per_source_currency`** | `REAL` | Monthly average bilateral exchange rate expressed as Malaysian Ringgit (MYR) per unit of source currency (from Bank Negara Malaysia). A higher value indicates source currency appreciation against MYR. |
| **`target_missing_flag`** *(imputed only)* | `INTEGER` | Binary flag (`1` = target arrivals figure was originally missing in raw release; `0` = observed). |
| **`model_row_status`** *(imputed only)* | `TEXT` | Competition split status: `Training eligible` (67,000 rows with historical actuals) or `Hold out - target not published` (2,040 rows reserved for forecasting). |

---

## 📈 Macroeconomic Time Series Variables (`imputed_time_series_data` & `original_time_series_data`)

Monthly external macroeconomic, commodity, and geopolitical risk indicators affecting tourism demand:

### 1. Calendar & Temporal Identifiers
* **`month`** (`TEXT`): Year-month identifier in `YYYY-MM-DD` format (e.g., `2017-03-01`).
* **`year`** (`INTEGER`): Calendar year (2017 to 2026).
* **`month_number`** (`INTEGER`): Calendar month index (1 to 12).

### 2. Geopolitical Risk (GPR) Indicators
* **`gpr_global_index`** (`REAL`): Global Geopolitical Risk Index (benchmark index developed by Caldara & Iacoviello measuring worldwide geopolitical tensions, armed conflicts, and terror threats).
* **`gpr_malaysia_index`** (`REAL`): Malaysia-specific Geopolitical Risk Index tracking regional geopolitical news sentiment and domestic stability.

### 3. Global Energy Commodity
* **`brent_crude_usd_bbl`** (`REAL`): Monthly average benchmark price of Brent Crude oil in US Dollars per barrel (`USD/bbl`), serving as a proxy for aviation jet fuel and long-haul travel costs.

### 4. Malaysian Macroeconomic Indices (DOSM / OpenDOSM)
* **`leading_index`** (`REAL`): Malaysian Leading Economic Index (anticipates short-term economic inflection points and turning trends).
* **`coincident_index`** (`REAL`): Malaysian Coincident Economic Index (gauges current economic activity and real-time output pace).
* **`lagging_index`** (`REAL`): Malaysian Lagging Economic Index (confirms medium- to long-term economic shifts).
* **`leading_diffusion_index`** (`REAL`): Diffusion index measuring the proportion of leading components expanding (% of components showing positive momentum).
* **`coincident_diffusion_index`** (`REAL`): Diffusion index measuring the proportion of coincident components expanding.

### 5. Domestic Retail Fuel Prices (Ministry of Finance / OpenDOSM)
* **`ron95_rm_litre_monthly_avg`** (`REAL`): Monthly average retail price of subsidized RON95 petrol in Malaysia (`RM/litre`), reflecting domestic land transportation and tour coach operating costs.
* **`ron97_rm_litre_monthly_avg`** (`REAL`): Monthly average retail price of market-driven RON97 petrol (`RM/litre`).
* **`diesel_peninsular_rm_litre_monthly_avg`** (`REAL`): Monthly average retail diesel price in Peninsular Malaysia (`RM/litre`).
* **`diesel_east_malaysia_rm_litre_monthly_avg`** (`REAL`): Monthly average retail diesel price in Sabah and Sarawak (`RM/litre`).

### 6. Ingestion, Completeness & Imputation Audit Flags
* **`gpr_observations_in_month`** (`INTEGER`): Count of daily GPR index observations recorded in that calendar month.
* **`brent_observations_in_month`** (`INTEGER`): Count of daily Brent trading sessions recorded in the month.
* **`mei_observations_in_month`** (`INTEGER`): Number of macroeconomic index observations extracted.
* **`fuel_source_observations_in_month`** (`INTEGER`): Number of fuel price records extracted from gazette sources.
* **`fuel_effective_days_in_month`** (`INTEGER`): Number of calendar days covered by fuel price determinations.
* **`period_days_in_file`** (`INTEGER`): Number of days present in the raw data extract.
* **`calendar_days_in_month`** (`INTEGER`): Total calendar days in that month (28, 29, 30, or 31).
* **`fuel_coverage_pct`** (`INTEGER`): Percentage of the month covered by published fuel gazettes.
* **`period_complete_flag`** (`INTEGER`): Binary indicator (`1` if entire month has full data coverage; `0` if incomplete).
* **`fuel_low_coverage_flag`** (`INTEGER`): Warning flag (`1` if fuel price data coverage was partial or sparse).
* **`retrieved_at_utc`** (`REAL`): UTC timestamp recording when the observation was extracted.
* **Predictor Imputation Flags** (`INTEGER`): Binary flags (`gpr_global_index_imputed_flag`, `gpr_malaysia_index_imputed_flag`, `brent_crude_usd_bbl_imputed_flag`, `leading_index_imputed_flag`, `coincident_index_imputed_flag`, `lagging_index_imputed_flag`, `leading_diffusion_index_imputed_flag`, `coincident_diffusion_index_imputed_flag`) denoting if that predictor was estimated.
* **`imputed_predictor_count`** (`INTEGER`): Total count of macroeconomic predictors imputed in that month (0 to 8).
* **`any_predictor_imputed_flag`** (`INTEGER`): Binary indicator (`1` if any predictor in the row was imputed; `0` if all observed).
* **`imputation_status`** (`TEXT`): Human-readable audit status (e.g., `All original observed`, `Imputed via forward-fill / linear interpolation`).

---

## 🏨 State Hotel Panel Variables (`hotel_state_annual_panel_data`)

Annual state-level hospitality operations and domestic visitor metrics covering 2017 to 2025 across all 16 states and federal territories:

| Variable Name | Data Type | Description & Meaning |
| :--- | :---: | :--- |
| **`date`** | `TEXT` | Calendar year-end date in `YYYY-MM-DD` format (`2017-12-31` to `2025-12-31`). |
| **`year`** | `INTEGER` | Calendar observation year (2017 to 2025, 9 consecutive annual periods). |
| **`state_code`** | `TEXT` | Standard ISO 3166-2:MY state identifier code (e.g., `MY-01` for Johor, `MY-14` for Kuala Lumpur). |
| **`state_name`** | `TEXT` | Official English name of the state or federal territory. |
| **`hotel_occupancy_rate_pct`** | `REAL` | Annual average hotel room occupancy rate expressed as a percentage (sourced from Tourism Malaysia KPI reports). |
| **`domestic_hotel_guests`** | `INTEGER` | Count of domestic Malaysian residents accommodated in hotels within the state. |
| **`international_hotel_guests`** | `INTEGER` | Count of foreign international travelers accommodated in hotels within the state. |
| **`total_hotel_guests`** | `INTEGER` | Aggregate hotel guests accommodated (`domestic_hotel_guests` + `international_hotel_guests`). |
| **`domestic_visitors`** | `INTEGER` | Total domestic visitor trips into the state (sourced from DOSM Survey of Domestic Tourism). |
| **`release_agency`** | `TEXT` | Custodian reporting agencies (*Tourism Malaysia* and *Department of Statistics Malaysia*). |
| **`source_document`** | `TEXT` | Formal publication name (e.g., *Tourism Malaysia KPI 2018–2025*, *DOSM Domestic Tourism Survey*). |
| **`source_url`** | `TEXT` | Official download or portal URL. |
| **`source_pages`** | `TEXT` | Specific report page citations. |
| **`data_quality_note`** | `TEXT` | Data quality and provenance audit notes (e.g., unit conversions from '000 to absolute headcounts, revised baseline notes). |

---

## 📖 Variable Provenance Catalog (`sources` table)

The `sources` table acts as the authoritative metadata dictionary mapping every variable code across all workbook sheets to official sources:

| Column Name | Description |
| :--- | :--- |
| **`workbook_sheet`** | Target Excel sheet where the variable appears (`Imputed Country Panel Data`, `Imputed Time Series Data`, `Hotel State Annual Panel Data`). |
| **`variable_code`** | Programmatic column name in the database. |
| **`variable_name`** | Formal descriptive name of the indicator. |
| **`what_it_comes_from`** | Functional description of the metric's source. |
| **`original_source_field_or_formula`** | Field name in the raw agency API or mathematical derivation formula. |
| **`release_agency`** | Custodian agency (e.g., *Department of Statistics Malaysia*, *Bank Negara Malaysia*, *Ministry of Finance*, *Tourism Malaysia*). |
| **`source_dataset_or_series`** | Official dataset publication or series title. |
| **`api_or_download_url_used`** | Live public URL or API endpoint used to retrieve the data. |
| **`access_method`** | Ingestion mechanism (e.g., `API query`, `Direct file download`, `Open data portal`). |
| **`source_classification`** | Category (e.g., `Panel Target`, `Macroeconomic Index`, `Exchange Rate`, `Commodity Price`, `Hospitality Metric`). |
| **`frequency`** | Temporal granularity (`Monthly`, `Daily aggregated to Monthly`, `Annual`). |
| **`measurement_unit`** | Unit of measure (`Persons`, `Index (2015=100)`, `MYR/Currency`, `USD/bbl`, `RM/litre`, `Percent`). |
| **`cleaning_or_derivation_applied`** | Transformations applied (e.g., `Monthly averaging`, `Forward-fill imputation`, `Standardization`, `Headcount unit conversion`). |
| **`original_missing_count`** | Number of missing values in the raw dataset. |
| **`original_missing_rate_pct`** | Missing data percentage prior to imputation. |
| **`final_missing_count`** | Missing data count in the final modeling table. |
| **`related_flag_or_important_note`** | Methodological notes or caveats for analysts and models. |

---

## 🗺️ Geographic & Market Classifications

### 1. International Source Markets (20 Countries)
* **ASEAN (7 Markets)**:
  * Brunei (`BRN` / BND), Indonesia (`IDN` / IDR), Myanmar (`MMR` / MMK), Philippines (`PHL` / PHP), Singapore (`SGP` / SGD), Thailand (`THA` / THB), Vietnam (`VNM` / VND).
* **Non-ASEAN (13 Markets)**:
  * Australia (`AUS` / AUD), Bangladesh (`BGD` / BDT), China (`CHN` / CNY), France (`FRA` / EUR), Germany (`DEU` / EUR), India (`IND` / INR), Japan (`JPN` / JPY), Nepal (`NPL` / NPR), Pakistan (`PAK` / PKR), South Korea (`KOR` / KRW), Taiwan (`TWN` / TWD), United Kingdom (`GBR` / GBP), United States (`USA` / USD).

### 2. Domestic State-Level Coverage (16 States & Federal Territories)
* **Peninsular Malaysia (13 States / Territories)**:
  * Johor (`MY-01`), Kedah (`MY-02`), Kelantan (`MY-03`), Melaka (`MY-04`), Negeri Sembilan (`MY-05`), Pahang (`MY-06`), Pulau Pinang (`MY-07`), Perak (`MY-08`), Perlis (`MY-09`), Selangor (`MY-10`), Terengganu (`MY-11`), W.P. Kuala Lumpur (`MY-14`), W.P. Putrajaya (`MY-16`).
* **East Malaysia (3 States / Territories)**:
  * Sabah (`MY-12`), Sarawak (`MY-13`), W.P. Labuan (`MY-15`).
