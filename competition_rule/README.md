# 📚 Competition Rule — DOSM Datathon 2026

**Theme**: Leveraging Machine Learning (ML) & Artificial Intelligence (AI) for Sustainable Tourism in Malaysia  
**Team**: Nexora  
**Group Focus**: Tourism Demand Forecasting, Macroeconomic Impact & Geopolitical Risk Analytics  
**Competition**: Department of Statistics Malaysia (DOSM) Datathon 2026  
**Official Competition Portal**: [https://datathon.dosm.gov.my/](https://datathon.dosm.gov.my/) *(Check for real-time announcements, schedules & forms)*

---

## 📁 Files

| File | Description |
| :--- | :--- |
| [`Datathon 2026 - Booklet Final.pdf`](./Datathon%202026%20-%20Booklet%20Final.pdf) | Official DOSM competition handbook: rules, eligibility, data integrity mandates, submission formats and calendar |
| [`DOSM_Datathon_2026_Final_Round_Rubric_EN.pdf`](./DOSM_Datathon_2026_Final_Round_Rubric_EN.pdf) | Official final-round marking scheme |

The submitted files live with each round: [`1_preliminary_round/submission/`](../1_preliminary_round/submission/) and [`2_final_round/submission/`](../2_final_round/submission/).

---

## 🌐 Official Competition Portal

Always verify the latest announcements, schedules, FAQs, and submission Google Forms at **[https://datathon.dosm.gov.my/](https://datathon.dosm.gov.my/)**.

* **Competition Schedules & Milestones**: Live timeline of preliminary evaluations, shortlisting announcements, and the grand finale.
* **Submission Google Form**: The mandatory confirmation form required after uploading preliminary deliverables.
* **Official Data Sets & OpenDOSM Portals**: [OpenDOSM](https://open.dosm.gov.my), [eStatistik](https://newss.statistics.gov.my), [StatsDW](https://statsdw.dosm.gov.my).
* **Rules & Updates**: Clarifications issued by the competition secretariat and technical committees.

---

## 📑 Booklet Summary

| Section | Key Guidance & Rule Set | Repository Reference |
| :--- | :--- | :--- |
| **Eligibility & Registration** | Open to registered teams (Team **Nexora**). | [`README.md`](../README.md) |
| **Deliverable 1: Report** | `Nexora_Datathon2026_Report.pdf`: Max 25 pages (excluding cover, TOC, references), Times New Roman 12, 1.5 spacing, justified. | [`1_preliminary_round/report/`](../1_preliminary_round/report/) |
| **Deliverable 2: Dashboard** | `Nexora_Datathon2026_Dashboard.zip`: Contains `Dashboard.pdf`, `Dashboard.pbix`, `Data.xlsx`, and `README.txt`. | [`1_preliminary_round/dashboard/`](../1_preliminary_round/dashboard/) |
| **Deliverable 3: Video** | `Nexora_Datathon2026_Video.mp4`: Strict 10-minute maximum MP4 presentation including live dashboard demo. | [`1_preliminary_round/submission/`](../1_preliminary_round/submission/) |
| **Preliminary Deadlines** | **File Upload**: 22 September 2026, 5:00 PM (Google Drive)<br>**Confirmation Form**: 22 September 2026, 11:59 PM | [Preliminary Round Submission Guide](#-preliminary-round-submission-guide) |
| **Final Round** | 10-minute live pitch including a dashboard demo, followed by 5 minutes of Q&A. | [`2_final_round/`](../2_final_round/) |
| **Data Compliance** | Genuine Malaysian data only. No simulated or fabricated data. Bonus evaluation for official government sources. | [`data/README.md`](../data/README.md) |

---

## 🏁 Final Round Marking Scheme

Source: [`DOSM_Datathon_2026_Final_Round_Rubric_EN.pdf`](./DOSM_Datathon_2026_Final_Round_Rubric_EN.pdf)

| Criterion | C1 PJT | C2 DEM | C3 ANL | C4 IMP | C5 INV |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Weight | 20% | 25% | 20% | 25% | 10% |

The dashboard demonstration counts inside the 10-minute pitch, followed by 5 minutes of Q&A.

---

## 📦 Preliminary Round Submission Guide

**Submission Location**: Team's Designated Google Drive Folder

### ⏰ Deadlines (22 September 2026)

| Milestone | Deadline | Requirement |
| :--- | :---: | :--- |
| **1. File Upload** | **5:00 PM** | All 3 files (`.pdf`, `.zip`, `.mp4`) uploaded to team Google Drive |
| **2. Confirmation Form** | **11:59 PM** | Mandatory confirmation Google Form submitted on [datathon.dosm.gov.my](https://datathon.dosm.gov.my/) |

> [!WARNING]
> File uploads strictly close at **5:00 PM**. The 11:59 PM cutoff applies only to the confirmation Google Form.

### 1. Written Project Report (`Nexora_Datathon2026_Report.pdf`)

* **Specifications**: PDF format | Max **25 pages** (strictly excluding Front page, Table of contents, References) | **Times New Roman 12 pt** | **1.5 line spacing** | **Justified alignment** | Official DOSM cover page template.
* **Required Structure**:
  1. **Front page** *(excluded from page count)*
  2. **Table of contents** *(excluded from page count)*
  3. **Introduction**: Background, Problem statement, Research objectives
  4. **Literature review**
  5. **Methodology and data-analysis methods**
  6. **Findings and results**: ML/AI results, Solution approach, Visualisations
  7. **Dashboard output**
  8. **Conclusion**
  9. **References** *(excluded from page count)*

### 2. Dashboard Package (`Nexora_Datathon2026_Dashboard.zip`)

*Local Workspace*: [`1_preliminary_round/dashboard/`](../1_preliminary_round/dashboard/)

Compress exactly these 4 files into the root of the ZIP:
1. **`Dashboard.pdf`**: High-resolution static view of all completed dashboard pages.
2. **`Dashboard.pbix`** *(or `.xlsx`/`.twbx`)*: Original interactive dashboard file (fully functional filters, slicers & drill-downs; zero broken calculations; self-contained without external database dependencies).
3. **`Data.xlsx`**: Consolidated source, forecast, backtest, and model-diagnostic data used by the dashboard.
4. **`README.txt`**: Plain-text document covering:
   - Software name and exact version (e.g., *Power BI Desktop September 2026*)
   - Step-by-step instructions to open the dashboard
   - Navigation guide (filters, slicers, cross-filtering, views)
   - Required plugins or add-ons (if any; zero external plugins recommended)
   - Assumptions and limitations (data boundaries, refresh states)

> [!NOTE]
> Static screenshots inside the written report do **not** replace the interactive dashboard file.

### 3. Video Presentation (`Nexora_Datathon2026_Video.mp4`)

* **Specifications**: **MP4** format | **Maximum 10 minutes** (strict cap) | Clear audio, crisp video resolution, legible text | Must demonstrate the live interactive dashboard.
* **Recommended Flow**:
  1. *Team & Project Intro* (within 1 min): Team Nexora, member introductions, project title.
  2. *Problem Statement & Objectives*: Challenge context and measurable goals.
  3. *Data Sources*: Malaysian data ecosystem overview.
  4. *Methodology & ML/AI Model*: Data pipeline, cleaning, models, validation metrics.
  5. *Key Findings & Insights*: Trend analysis, model results, and implications.
  6. *Live Dashboard Demo*: Screen recording of interactive filters, scenarios, and user flow.
  7. *Conclusion & Impact*: Recommendations, potential socio-economic impact, scalability.

### ✅ Submission Checklist

- [x] **Report**: `Nexora_Datathon2026_Report.pdf` (23 counted pages; 29 PDF pages including 1 cover, 2 TOC, and 3 reference pages; Times New Roman 12 pt; 1.5 spacing; justified)
- [x] **Dashboard**: `Nexora_Datathon2026_Dashboard.zip` (contains exactly `Dashboard.pdf`, `Dashboard.pbix`, `Data.xlsx`, and `README.txt` at the ZIP root)
- [x] **Video**: `Nexora_Datathon2026_Video.mp4` (8:46, 1920 × 1080, H.264 video and AAC audio)
- [x] **Drive Upload** and **Confirmation Form** completed; Team Nexora advanced to the final round.

---

## ⚖️ Data Rules & Compliance

* **Malaysia-Centric**: All raw data must originate from / relate to Malaysia (foreign data permitted solely for comparative context).
* **Authenticity**: Use genuine, publicly accessible data. **Fabricated or simulated data is strictly prohibited.**
* **Bonus Points**: Extra marks awarded for using official Malaysian sources (OpenDOSM, eStatistik, StatsDW, Tourism Malaysia, BNM).
* **Attribution & Privacy**: Transparently cite all data, APIs, and libraries; zero confidential or unpermitted personal data (PII).

---

## ℹ️ Preliminary vs. Final Round

Presentation slide decks were **not** required for the preliminary round. Team Nexora was shortlisted for the final round, a physical live pitch (10-minute presentation + 5-minute Q&A). The final-round slides, dashboard and script are in [`2_final_round/`](../2_final_round/).
