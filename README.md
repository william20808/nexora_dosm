# 🇲🇾 DOSM Datathon 2026

**Theme**: Leveraging Machine Learning (ML) & Artificial Intelligence (AI) for Sustainable Tourism in Malaysia  
**Team**: Nexora  
**Group Focus**: Tourism Demand Forecasting, Macroeconomic Impact & Geopolitical Risk Analytics  
**Problem Statement**: How does geopolitical risk affect the tourism industry in Malaysia? 

**Organiser**: Department of Statistics Malaysia (DOSM)  
**Official Portal**: [https://datathon.dosm.gov.my/](https://datathon.dosm.gov.my/) *(Official updates, announcements & forms)*  
**Competition Rulebook**: [`competition and submission/rulebook/Datathon 2026 - Booklet Final.pdf`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/competition%20and%20submission/rulebook/Datathon%202026%20-%20Booklet%20Final.pdf)

---

## 🎯 Executive Overview

This repository houses the analytical models, data engineering pipelines, interactive Power BI dashboard workspace, and preliminary round submission documentation for **Team Nexora**. The project integrates a 10-year monthly dataset (March 2017 to September 2026) spanning **20 international source markets** alongside an annual state-level hospitality panel (**16 Malaysian states and territories**, 2017–2025) to model and forecast tourism demand patterns in Malaysia under the influence of bilateral exchange rates, global fuel prices, and geopolitical risk factors.

---

## 📦 Preliminary Round Deliverables & Deadlines

> **Submission Location**: Team Nexora's designated Google Drive folder  
> **File Upload Deadline**: **22 September 2026, 5:00 PM** *(Upload all files prior to this cutoff)*  
> **Confirmation Google Form Deadline**: **22 September 2026, 11:59 PM** *(Submit form via portal)*  

| Deliverable | Official Filename | Format | Description | Dedicated Directory |
| :--- | :--- | :---: | :--- | :---: |
| **1. Written Report** | `Nexora_Datathon2026_Report.pdf` | `.pdf` | Max 25 pages, official DOSM front-page template, Times New Roman 12, 1.5 line spacing | [`report/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/report) |
| **2. Dashboard Package** | `Nexora_Datathon2026_Dashboard.zip` | `.zip` | Compressed package containing `Dashboard.pbix`, `Dashboard.pdf`, `Data.csv`, and `README.txt` | [`powerbi_dashboard/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/powerbi_dashboard) |
| **3. Video Presentation** | `Nexora_Datathon2026_Video.mp4` | `.mp4` | Max 10 minutes MP4 video presenting methodology, findings, and working dashboard demo | [`competition and submission/submission/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/competition%20and%20submission/submission) |

---

## 📁 Repository Structure

```text
nexora_dosm/
├── README.md                                         # Master repository overview & navigation
├── requirements.txt                                  # Python dependencies
├── .gitignore                                        # Ignored temporary files & local caches
├── competition and submission/
│   ├── README.md                                     # Workspace hub & portal links
│   ├── rulebook/
│   │   ├── README.md                                 # Summary of rules, timeline & scoring rubrics
│   │   └── Datathon 2026 - Booklet Final.pdf         # Official DOSM competition handbook (PDF)
│   └── submission/
│       └── README.md                                 # Preliminary round packaging guidelines & master checklist
├── data/
│   ├── README.md                                     # Complete data catalog, schema & variable dictionary
│   ├── dosm_datathon.db                              # Relational SQLite database (6 indexed tables & 3 views)
│   ├── schema.sql                                    # Database DDL table definitions, indexes & views
│   ├── queries.sql                                   # 20 data viewing, auditing & feature engineering SQL queries
│   └── excel data/
│       └── final_deliveries_dataset.xlsx             # Master Excel workbook (6 sheets incl. Sources)
├── machine_learning/
│   ├── README.md                                     # Machine learning pipeline documentation
│   ├── features/
│   │   └── feature_engineering.py                    # Temporal lags, rolling statistics & interaction pipeline
│   ├── models/
│   │   ├── train.py                                  # Model training & cross-validation routines
│   │   └── predict.py                                # Forecast generation for the hold-out evaluation set
│   └── evaluation/
│       ├── evaluate.py                               # Validation metrics (MAPE, RMSE, MAE)
│       └── explainability.py                         # Feature importance & sensitivity analysis
├── powerbi_dashboard/
│   ├── README.md                                     # Power BI staging workspace documentation
│   ├── README.txt                                    # Plain-text user instructions for ZIP deliverable
│   ├── Dashboard.pbix                                # Interactive Power BI report
│   ├── Dashboard.pdf                                 # High-resolution static report export
│   └── Data.csv                                      # Underlying flat dataset powering the visuals
└── report/
    ├── README.md                                     # Report specifications & section page budget allocation
    └── doc_link.txt                                  # Collaborative OneDrive Word template link
```

---

## 🗂️ Core Project Modules

### 1. Competition & Submission Hub ([`competition and submission/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/competition%20and%20submission))
Houses all competition-level materials organized into two subfolders:
* **Rulebook** ([`competition and submission/rulebook/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/competition%20and%20submission/rulebook)): The official DOSM competition handbook ([`Datathon 2026 - Booklet Final.pdf`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/competition%20and%20submission/rulebook/Datathon%202026%20-%20Booklet%20Final.pdf)) and quick rules reference.
* **Submission** ([`competition and submission/submission/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/competition%20and%20submission/submission)): Preliminary round packaging guidelines, file naming conventions, upload deadlines, and verification checklist.
Always monitor [https://datathon.dosm.gov.my/](https://datathon.dosm.gov.my/) for live updates.

### 2. Data Ecosystem ([`data/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/data))
Houses the SQLite database (`dosm_datathon.db`), master Excel dataset (`final_deliveries_dataset.xlsx`), schema DDL, and SQL query suite. The repository integrates monthly country arrivals (20 source markets), macroeconomic and geopolitical time series, and 16-state annual hotel performance data (2017–2025). Complete variable definitions and data catalogs are documented in [`data/README.md`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/data/README.md).

### 3. Machine Learning ([`machine_learning/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/machine_learning))
Modular pipeline workspace for feature engineering, model training, and performance evaluation. Module outlines and workflow structures are documented in [`machine_learning/README.md`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/machine_learning/README.md).

### 4. Power BI Dashboard ([`powerbi_dashboard/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/powerbi_dashboard))
Staging workspace for building and packaging the interactive Power BI dashboard deliverable (`Nexora_Datathon2026_Dashboard.zip`). Staging requirements are documented in [`powerbi_dashboard/README.md`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/powerbi_dashboard/README.md).

### 5. Written Report ([`report/`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/report))
Workspace for drafting the written project report (`Nexora_Datathon2026_Report.pdf`), including the collaborative Word template workspace link and formatting rules in [`report/README.md`](file:///c:/Users/user/Desktop/CS50/CS50W%20-%20Web/nexora_dosm/report/README.md).
