# 🇲🇾 DOSM Datathon 2026

**Project**: Geopolitical Risk and International Tourism Demand in Malaysia: A Machine Learning Forecasting Framework for 20 Source Markets  
**Team**: Nexora  
**Members**: Chin William | Tang Xin Yi | Janis Ong Jing Yao | Tee Xin Yee  
**Advisor**: Dr. Kelwin Tan Seen Tiong, Universiti Tunku Abdul Rahman (UTAR)  
**Theme**: Leveraging Machine Learning and Artificial Intelligence for Sustainable Tourism in Malaysia  
**Focus**: Tourism demand forecasting, economic drivers, and geopolitical-risk analytics  
**Organiser**: Department of Statistics Malaysia (DOSM)  
**Official Portal**: [datathon.dosm.gov.my](https://datathon.dosm.gov.my/)

---

## 📦 Submissions

| Round | Deliverable | File |
| :--- | :--- | :--- |
| **1 · Preliminary** | Written report | [`Nexora_Datathon2026_Report.pdf`](1_preliminary_round/submission/Nexora_Datathon2026_Report.pdf) |
| | Dashboard package | [`Nexora_Datathon2026_Dashboard.zip`](1_preliminary_round/submission/Nexora_Datathon2026_Dashboard.zip) |
| | Video presentation (8:46, 1080p) | [`Nexora_Datathon2026_Video.mp4`](1_preliminary_round/submission/Nexora_Datathon2026_Video.mp4) |
| **2 · Final pitch** | Presentation slides | [`PPTX`](2_final_round/submission/Nexora%20-%20DOSM%20Datathon%202026%20Presentation%20Slides.pptx) · [`PDF`](2_final_round/submission/Nexora%20-%20DOSM%20Datathon%202026%20Presentation%20Slides.pdf) |
| | Dashboard | [`PBIX`](2_final_round/submission/Nexora%20-%20DOSM%20Datathon%202026%20Dashboard.pbix) · [`PDF`](2_final_round/submission/Nexora%20-%20DOSM%20Datathon%202026%20Dashboard.pdf) |

Each round's `submission/` folder holds exactly the files that were handed in, under their submitted names. Rules, the final-round marking scheme and the preliminary submission guide are in [`competition_rule/`](competition_rule/README.md).

---

## 🎯 Project Overview

This project evaluates the predictive relationship between geopolitical risk and international tourism demand in Malaysia. It combines monthly arrivals from 20 modelled source markets with bilateral exchange rates, geopolitical-risk indices, energy prices, lagged demand, and seasonal features.

The machine-learning pipeline produces one-to-four-month forecasts using a pooled direct multi-horizon LightGBM model. Its performance is compared with naive-last, seasonal-naive, and Ridge-regression benchmarks through rolling-origin backtesting. Results are presented in an interactive Power BI dashboard, documented in the written report, and pitched in the final round.

All aggregated arrival figures refer only to the 20 modelled source markets and must not be interpreted as Malaysia's complete international-arrival total.

---

## 🔀 Project Flow

```text
 data/  ──►  machine_learning/  ──►  dashboard  ──►  report  ──►  pitch
 (SQLite      (features, LightGBM,     (Power BI)     (Round 1)    (Round 2)
  + Excel)     backtests, SHAP)
```

---

## 📁 Repository Structure

```text
nexora_dosm/
├── README.md
├── LICENSE                        # MIT licence
├── requirements.txt
├── competition_rule/              # Official rules and marking schemes
│   ├── README.md
│   ├── Datathon 2026 - Booklet Final.pdf
│   └── DOSM_Datathon_2026_Final_Round_Rubric_EN.pdf
├── data/                          # 1 · Source data
│   ├── README.md
│   ├── dosm_datathon.db
│   ├── schema.sql
│   ├── queries.sql
│   └── excel data/
│       └── final_deliveries_dataset.xlsx
├── machine_learning/              # 2 · Forecasting pipeline
│   ├── README.md
│   ├── DATA_DICTIONARY.md
│   ├── __init__.py
│   ├── config.py, data_loader.py, feature_engineering.py
│   ├── train.py, predict.py, evaluate.py, explainability.py
│   ├── run_pipeline.py
│   ├── artifacts/
│   └── outputs/
├── 1_preliminary_round/           # 3 · Report, dashboard and video
│   ├── submission/                # Submitted files (PDF, ZIP, MP4)
│   ├── report/                    # Editable report DOCX
│   ├── dashboard/                 # Unzipped dashboard package source
│   └── slides/                    # Preliminary presentation PPTX
└── 2_final_round/                 # 4 · Live pitch
    ├── submission/                # Submitted slides and dashboard
    ├── script/                    # Pitch script, judge Q&A and project guide
    └── assets/                    # Slide images, icons and video clips
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

### Preliminary Round

The [`1_preliminary_round/`](1_preliminary_round/) directory contains the submitted report, dashboard ZIP and video, together with:

- `report/` — the editable report DOCX (23 counted pages, Sections 1.0–6.0).
- `dashboard/` — the unzipped Power BI package; [`README.txt`](1_preliminary_round/dashboard/README.txt) explains how to open and navigate it.
- `slides/` — the preliminary slide deck.

### Final Round

The [`2_final_round/`](2_final_round/) directory contains the submitted pitch slides and final dashboard, the images, icons and video clips used in the deck. The slide videos are embedded in the PPTX, so the deck plays without the `assets/` folder. The final dashboard is an updated version of the preliminary one.

The [`script/`](2_final_round/script/) folder holds the team's presentation preparation:

- [`presentation_script_revised.pdf`](2_final_round/script/presentation_script_revised.pdf) — the spoken script for the 12 slides and the live demo, with click cues, timings (about 9:15) and marking-scheme coverage.
- [`judge_qa_preparation.pdf`](2_final_round/script/judge_qa_preparation.pdf) — 30 likely judge questions with short answers; ★ marks the most important.
- [`Nexora_Project_Guide.pdf`](2_final_round/script/Nexora_Project_Guide.pdf) — a plain-language guide to the whole project, following the report from problem to results.

### Competition Materials

The [`competition_rule/`](competition_rule/) directory contains the official booklet, the final-round marking scheme, and a README that summarises the rules and the preliminary submission guide.

---

## 📄 License

This project is released under the [MIT License](LICENSE).
