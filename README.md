# 🇲🇾 DOSM Datathon 2026

**Project**: Geopolitical Risk and International Tourism Demand in Malaysia: A Machine Learning Forecasting Framework for 20 Source Markets  
**Team**: Nexora  
**Theme**: Leveraging Machine Learning and Artificial Intelligence for Sustainable Tourism in Malaysia  
**Focus**: Tourism demand forecasting, economic drivers, and geopolitical-risk analytics  
**Organiser**: Department of Statistics Malaysia (DOSM)  
**Official Portal**: [datathon.dosm.gov.my](https://datathon.dosm.gov.my/)  
**Competition Rulebook**: [`competition and submission/rulebook/Datathon 2026 - Booklet Final.pdf`](competition%20and%20submission/rulebook/Datathon%202026%20-%20Booklet%20Final.pdf)

---

## 🎯 Project Overview

This project evaluates the predictive relationship between geopolitical risk and international tourism demand in Malaysia. It combines monthly arrivals from 20 modelled source markets with bilateral exchange rates, geopolitical-risk indices, energy prices, lagged demand, and seasonal features.

The machine-learning pipeline produces one-to-four-month forecasts using a pooled direct multi-horizon LightGBM model. Its performance is compared with naive-last, seasonal-naive, and Ridge-regression benchmarks through rolling-origin backtesting. Results are presented in an interactive Power BI dashboard and documented in the written project report.

All aggregated arrival figures refer only to the 20 modelled source markets and must not be interpreted as Malaysia's complete international-arrival total.

---

## 📦 Submission Deliverables

Final submission artifacts are stored in [`competition and submission/submission/`](competition%20and%20submission/submission/).

| Deliverable | Official filename | Description |
| :--- | :--- | :--- |
| Written report | `Nexora_Datathon2026_Report.pdf` | Final competition report in PDF format |
| Dashboard package | `Nexora_Datathon2026_Dashboard.zip` | Power BI dashboard, static PDF, source data, and usage instructions |
| Video presentation | `Nexora_Datathon2026_Video.mp4` | Final 8-minute 46-second, 1080p presentation video |

The editable report and presentation deck are maintained in [`report and slide/`](report%20and%20slide/).

---

## 📁 Repository Structure

```text
nexora_dosm/
├── README.md
├── requirements.txt
├── competition and submission/
│   ├── README.md
│   ├── rulebook/
│   │   ├── README.md
│   │   ├── SUBMISSION_README.md
│   │   └── Datathon 2026 - Booklet Final.pdf
│   └── submission/
│       ├── Nexora_Datathon2026_Report.pdf
│       ├── Nexora_Datathon2026_Dashboard.zip
│       └── Nexora_Datathon2026_Video.mp4
├── data/
│   ├── README.md
│   ├── dosm_datathon.db
│   ├── schema.sql
│   ├── queries.sql
│   └── excel data/
│       └── final_deliveries_dataset.xlsx
├── machine_learning/
│   ├── README.md
│   ├── DATA_DICTIONARY.md
│   ├── config.py
│   ├── data_loader.py
│   ├── run_pipeline.py
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   ├── artifacts/
│   └── outputs/
├── powerbi_dashboard/
│   ├── Dashboard.pbix
│   ├── Dashboard.pdf
│   ├── Data.xlsx
│   ├── README.md
│   └── README.txt
└── report and slide/
    ├── README.md
    ├── Nexora_Datathon2026_Report.docx
    └── Nexora_Datathon2026_Presentation_Slide.pptx
```

---

## 🤖 Reproducing the Machine Learning Pipeline

Install the pinned dependencies and run the complete workflow from the repository root:

```bash
pip install -r requirements.txt
python -m machine_learning.run_pipeline
```

The pipeline reads `data/dosm_datathon.db`, regenerates the tables in `machine_learning/outputs/`, and writes the trained model to `machine_learning/artifacts/`. See [`machine_learning/README.md`](machine_learning/README.md) for the methodology summary, validation design, and detailed commands. Column definitions are documented in [`machine_learning/DATA_DICTIONARY.md`](machine_learning/DATA_DICTIONARY.md).

---

## 📊 Project Components

### Data

The [`data/`](data/) directory contains the SQLite database, schema, reusable SQL queries, and source Excel workbook. Its contents cover monthly source-market arrivals, exchange rates, geopolitical-risk indicators, energy prices, and supporting Malaysian tourism data.

### Machine Learning

The [`machine_learning/`](machine_learning/) directory contains feature engineering, model training, forecasting, evaluation, explainability, generated outputs, and the consolidated data dictionary.

### Power BI Dashboard

The [`powerbi_dashboard/`](powerbi_dashboard/) directory contains the editable Power BI report, static PDF export, consolidated Excel data source, and dashboard instructions.

### Report and Presentation Slides

The [`report and slide/`](report%20and%20slide/) directory contains the editable report DOCX, presentation PPTX, and report guidance. The final report PDF is stored with the official deliverables in the submission directory.

### Competition Materials

The [`competition and submission/rulebook/`](competition%20and%20submission/rulebook/) directory contains the official booklet, rule summary, and submission guide. The [`submission/`](competition%20and%20submission/submission/) directory contains only final submission artifacts.
