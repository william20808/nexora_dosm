# nexora_dosm

Department of Statistics Malaysia (DOSM) Datathon — Tourism Forecasting & Economic Analytics Repository.

---

## 📁 Repository Structure

```text
nexora_dosm/
├── README.md
├── requirements.txt
├── .gitignore
├── database/
│   ├── dosm_datathon.db                                  # SQLite database containing full time-series & panel tables
│   ├── monthly_shared_predictors_corrected_mar2017.xlsx  # Official source Excel workbook (138,000+ rows)
│   ├── schema.sql                                        # Table definitions (DDL) and indexing structure
│   └── queries.sql                                       # Analytical and feature extraction queries
├── src/
│   ├── features/
│   │   └── feature_engineering.py
│   ├── models/
│   │   ├── train.py
│   │   └── predict.py
│   └── evaluation/
│       ├── evaluate.py
│       └── explainability.py
└── dashboard/
    ├── Dashboard.pbix
    ├── Dashboard.pdf
    ├── Data.csv
    └── README.txt
```

---

## 🗄️ Database Architecture (`database/dosm_datathon.db`)

The SQLite database integrates historical tourism arrivals across **20 international source markets** alongside Malaysian macroeconomic and global geopolitical risk indicators spanning **March 2017 to September 2026** (10 years).

| Table Name | Source Sheet | Rows | Columns | Key Dimensions & Usage |
| :--- | :--- | :---: | :---: | :--- |
| **`imputed_panel_data`** | Imputed Panel Data (2) | **69,040** | **12** | Primary modeling table. Daily/monthly tourist arrivals by country with currency exchange rates (MYR), market segment, and train/hold-out labels. |
| **`original_panel_data`** | Original Data (2) | **69,040** | **10** | Un-imputed ground truth panel observations. |
| **`imputed_time_series_data`** | Imputed Time Series Data | **115** | **37** | Monthly external macroeconomic indicators: Brent Crude, RON95/RON97 fuel prices, Leading Economic Index, and Geopolitical Risk (GPR) indices. |
| **`original_time_series_data`** | Original Data | **115** | **26** | Un-imputed monthly macroeconomic and geopolitical time series. |

### Indexed Columns
- `imputed_panel_data`: `(source_country_iso3, date)`, `(source_country_iso3, year, month)`
- `imputed_time_series_data`: `(year, month_number)`, `(month)`

---

## 📊 Dataset Overview & Machine Learning Split

- **Origin Markets (20 countries)**:
  - **ASEAN**: Singapore (`SGP`), Indonesia (`IDN`), Thailand (`THA`), Brunei (`BRN`), Philippines (`PHL`), Vietnam (`VNM`), etc.
  - **Non-ASEAN**: China (`CHN`), India (`IND`), South Korea (`KOR`), Australia (`AUS`), Taiwan (`TWN`), Japan (`JPN`), United Kingdom (`GBR`), United States (`USA`), etc.
- **Top Source Markets by Volume**: Singapore (42.3%), Indonesia (14.6%), China (12.0%), Thailand (7.5%), Brunei (4.8%).
- **Dataset Partition (`model_row_status`)**:
  - **`Training eligible`**: **67,000 rows (97.05%)** — Historical ground truth for feature engineering, model training, and backtesting.
  - **`Hold out - target not published`**: **2,040 rows (2.95%)** — Reserved competition test horizon for final forecast evaluation.

---

## 🔍 Analytical SQL Queries (`database/queries.sql`)

Key queries ready to execute against `database/dosm_datathon.db`:

1. **Macroeconomic & Geopolitical Join**: Aligns tourist volume with Brent Crude, local fuel prices, leading economic index, and GPR indices.
2. **Market Share Ranking**: Ranks inbound tourist volume by origin country and market segment.
3. **Seasonality Breakdown**: Analyzes average inbound patterns across calendar months (1 to 12).
4. **ASEAN vs Non-ASEAN Comparison**: Compares inbound trends across regional markets over time.
5. **FX Sensitivity**: Measures the relationship between currency exchange rates (`monthly_myr_per_source_currency`) and tourist volumes.
6. **Training vs Hold-Out Split**: Audits rows designated for model training versus hold-out scoring.
7. **Post-Pandemic Recovery Tracker**: Benchmarks pre-pandemic (2019) volume against post-2023 recovery trajectories.

---

## 🚀 Quick Start: Connecting via Python

```python
import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("database/dosm_datathon.db")

# Example: Extract monthly arrivals joined with macroeconomic predictors
query = """
SELECT 
    p.year,
    p.month,
    ROUND(SUM(p.monthly_tourist_arrivals), 0) AS total_arrivals,
    ROUND(m.brent_crude_usd_bbl, 2) AS brent_crude,
    ROUND(m.leading_index, 2) AS leading_index
FROM imputed_panel_data p
LEFT JOIN imputed_time_series_data m 
  ON p.year = m.year AND p.month = m.month_number
WHERE p.model_row_status = 'Training eligible'
GROUP BY p.year, p.month
ORDER BY p.year, p.month;
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
