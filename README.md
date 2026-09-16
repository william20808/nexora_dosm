# nexora_dosm

**Team**: Nexora  
**Event**: Department of Statistics Malaysia (DOSM) Datathon 2026 — Tourism Forecasting & Economic Analytics Repository.

---

## 📁 Repository Structure

```text
nexora_dosm/
├── README.md                                         # Project documentation & overview
├── requirements.txt                                  # Environment dependencies
├── .gitignore                                        # Ignored local files & caches
├── data/
│   ├── dosm_datathon.db                              # SQLite database (panel, time series & sources)
│   ├── schema.sql                                    # Database table DDL & indexes
│   ├── queries.sql                                   # SQL analytics & ML feature engineering queries
│   └── excel data/
│       └── dataset.xlsx                              # Master Excel dataset (5 sheets incl. Sources)
├── report/
│   ├── README.md                                     # Report specifications & section page allocations
│   └── doc_link.txt                                  # Collaborative OneDrive Word template link
├── src/
│   ├── features/
│   │   └── feature_engineering.py                    # Feature generation pipeline
│   ├── models/
│   │   ├── train.py                                  # Model training routines
│   │   └── predict.py                                # Forecast generation for hold-out set
│   └── evaluation/
│       ├── evaluate.py                               # Metrics (MAPE, RMSE, MAE)
│       └── explainability.py                         # Model explainability & sensitivity
└── dashboard/
    ├── Dashboard.pbix                                # Power BI interactive dashboard
    ├── Dashboard.pdf                                 # Exported dashboard overview
    ├── Data.csv                                      # Exported dashboard dataset
    └── README.txt                                    # Dashboard notes
```

---

## 📑 Deliverable 1: Written Project Report

* **Document File**: `Nexora_Datathon2026_Report.pdf`
* **Word Template Workspace**: [Nexora_Datathon2026_Report_Template.docx](https://1drv.ms/w/c/4be9614aa70f8b63/IQAQPik3Zq4KQbo5MU3Go8-TAT6cTaHvKwVgnpJljTzj6co?e=rVGqJI) (Stored in [`report/doc_link.txt`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/report/doc_link.txt))
* **Page Budget**: Maximum **25 pages** (excluding Front page, Table of contents, References)
* **Typography**: Times New Roman 12 pt, 1.5 line spacing, Justified alignment
* **Detailed Guide**: See [`report/README.md`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/report/README.md)

### Report Section Architecture
1. **Front page** *(Excluded)*: Project Title, Team Nexora, Author Details, Academic Advisor
2. **Table of contents** *(Excluded)*: Automated Table of Contents
3. **1.0 INTRODUCTION** *(3 pages)*
   * 1.1 Background of the Study
   * 1.2 Problem Statement
   * 1.3 Research Objectives
4. **2.0 LITERATURE REVIEW** *(4 pages)*
   * 2.1 Geopolitical risk and tourism demand
   * 2.2 Oil Prices, Transport Costs and Tourism Demand
   * 2.3 Exchange Rates and Malaysia’s Destination Affordability
   * 2.4 Malaysian Tourism Resilience, Economic Conditions and SDG Alignment
   * 2.5 Machine-Learning Approaches and Research Gap
5. **3.0 METHODOLOGY AND DATA ANALYSIS METHODS** *(5 pages)*
   * 3.1 Data Collection and Sources
   * 3.2 Data Cleaning and Preprocessing
   * 3.3 Data Integration and Harmonisation
   * 3.4 Data Analysis Methods
   * 3.5 Machine Learning and Artificial Intelligence Methods
   * 3.6 Model Validation and Evaluation
6. **4.0 FINDINGS AND RESULTS** *(8 pages)*
   * 4.1 Machine Learning and Artificial Intelligence Results
   * 4.2 Solution Approach
   * 4.3 Visualisations
7. **5.0 DASHBOARD OUTPUT** *(3 pages)*
   * 5.1 Dashboard Overview
   * 5.2 Dashboard Functions and Interactivity
   * 5.3 Dashboard Visuals
8. **6.0 CONCLUSION** *(2 pages)*
9. **REFERENCES** *(Excluded)*

---

## 🗄️ Database Architecture (`data/dosm_datathon.db`)

The SQLite database integrates historical tourism arrivals across **20 international source markets** alongside Malaysian macroeconomic and global geopolitical risk indicators spanning **March 2017 to September 2026** (10 years).

| Table Name | Source Sheet | Rows | Columns | Key Dimensions & Usage |
| :--- | :--- | :---: | :---: | :--- |
| **`imputed_panel_data`** | Imputed Panel Data (2) | **69,040** | **12** | Primary modeling table: tourist arrivals by country with bilateral FX rates (MYR), market segment, and train/hold-out labels. |
| **`original_panel_data`** | Original Data (2) | **69,040** | **10** | Un-imputed ground truth panel observations. |
| **`imputed_time_series_data`** | Imputed Time Series Data | **115** | **37** | Monthly external macroeconomic indicators: Brent Crude, RON95/RON97, Diesel, Economic Indices, and GPR indices. |
| **`original_time_series_data`** | Original Data | **115** | **26** | Un-imputed monthly macroeconomic and geopolitical time series. |
| **`sources`** | Sources | **49** | **17** | Data dictionary and provenance catalog mapping every variable to official source APIs, agencies, units, and derivation rules. |

### Indexed Columns
- `imputed_panel_data`: `(source_country_iso3, date)`, `(source_country_iso3, year, month)`
- `imputed_time_series_data`: `(year, month_number)`, `(month)`
- `original_panel_data`: `(source_country_iso3, date)`, `(source_country_iso3, year, month)`
- `original_time_series_data`: `(year, month_number)`, `(month)`
- `sources`: `(workbook_sheet, variable_code)`

---

## 📊 Dataset Overview & Machine Learning Split

* **Origin Markets (20 countries)**:
  * **ASEAN (7)**: Brunei (`BRN`), Indonesia (`IDN`), Myanmar (`MMR`), Philippines (`PHL`), Singapore (`SGP`), Thailand (`THA`), Vietnam (`VNM`).
  * **Non-ASEAN (13)**: Australia (`AUS`), Bangladesh (`BGD`), China (`CHN`), France (`FRA`), Germany (`DEU`), India (`IND`), Japan (`JPN`), Nepal (`NPL`), Pakistan (`PAK`), South Korea (`KOR`), Taiwan (`TWN`), United Kingdom (`GBR`), United States (`USA`).
* **Dataset Partition (`model_row_status`)**:
  * **`Training eligible`**: **67,000 rows (97.05%)** — Historical observations with published arrivals for feature engineering and model training.
  * **`Hold out - target not published`**: **2,040 rows (2.95%)** — Evaluation horizon for generating final competition forecasts.

---

## 🔍 Analytical & Feature Engineering SQL Suite (`data/queries.sql`)

The repository includes a comprehensive 17-query SQL suite organized into three parts:

### Part 1: Data Viewing & Auditing (Data Engineering Checks)
1. **1.1 Variable Provenance & Metadata Lookup**: Inspects source agencies, APIs, and missing rates.
2. **1.2 Panel Balance & Temporal Coverage**: Verifies equal date distribution across all 20 origin countries.
3. **1.3 Imputation Audit**: Compares raw versus imputed time series predictors side-by-side.
4. **1.4 Target Availability Partition**: Audits training vs. hold-out evaluation row counts.
5. **1.5 Country & Currency Master List**: Reference lookup for origin markets and currency codes.

### Part 2: Exploratory Data Analysis (EDA & Statistical Aggregations)
6. **2.1 Source Market Volume Ranking**: Summary statistics (min, max, mean, market share %).
7. **2.2 Seasonality Analysis**: Arrival patterns across calendar months (Jan–Dec).
8. **2.3 Regional Dynamics**: ASEAN vs. Non-ASEAN volume comparisons over time.
9. **2.4 Currency Exchange Rate Volatility**: Bilateral FX rates, minimums, maximums, and annual spread.
10. **2.5 Macroeconomic Time Series**: Consolidated view of fuel prices, indices, and GPR.
11. **2.6 Historical Benchmark**: 2019 baseline vs. recovery tracking.

### Part 3: Feature Engineering (Machine Learning Preparation)
12. **3.1 Time-Series Lag Generation**: Autoregressive lags ($t-1, t-2, t-3, t-6, t-12$) via window functions.
13. **3.2 Rolling Window Statistics**: Trailing 3-month and 6-month moving averages & momentum ratios.
14. **3.3 Growth Rate Indicators**: Month-over-Month (% MoM) and Year-over-Year (% YoY) growth calculations.
15. **3.4 Interaction Terms**: Cross-features ($\text{FX} \times \text{Oil}$, Fuel-to-FX ratio, Index ratios).
16. **3.5 Master Training Feature Matrix**: Complete joined dataset ready for `pd.read_sql()` training.
17. **3.6 Master Hold-Out Feature Matrix**: Identical feature structure for generating competition predictions.

---

## 🚀 Quick Start: Connecting via Python

```python
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("data/dosm_datathon.db")

# Example: Extract master training dataset with engineered lags and macroeconomic predictors
query = """
SELECT * 
FROM (
    -- Execute Query 3.5 from data/queries.sql
    SELECT 
        p.year, p.month, p.source_country_iso3, p.source_country_name,
        p.market_segment, p.source_currency_code,
        p.monthly_tourist_arrivals AS target_arrivals,
        p.monthly_myr_per_source_currency,
        m.brent_crude_usd_bbl, m.ron95_rm_litre_monthly_avg,
        m.leading_index, m.gpr_global_index
    FROM imputed_panel_data p
    LEFT JOIN imputed_time_series_data m 
      ON p.year = m.year AND p.month = m.month_number
    WHERE p.model_row_status = 'Training eligible'
    GROUP BY p.source_country_iso3, p.year, p.month
)
LIMIT 10;
"""

df = pd.read_sql_query(query, conn)
print(df.head())
conn.close()
```

---

## 📦 Setup & Dependencies

Install dependencies using Python 3.10+:

```bash
pip install -r requirements.txt
```
