# 📚 Competition Rule — DOSM Datathon 2026

Official rules and marking schemes for the DOSM Datathon 2026 (Team Nexora). Official portal: [datathon.dosm.gov.my](https://datathon.dosm.gov.my/).

---

## 📁 Files

| File | Description |
| :--- | :--- |
| [`Datathon 2026 - Booklet Final.pdf`](./Datathon%202026%20-%20Booklet%20Final.pdf) | Official DOSM competition handbook: rules, eligibility, data integrity mandates, submission formats and calendar |
| [`DOSM_Datathon_2026_Final_Round_Rubric_EN.pdf`](./DOSM_Datathon_2026_Final_Round_Rubric_EN.pdf) | Official final-round marking scheme |

The submitted files live with each round: [`1_preliminary_round/submission/`](../1_preliminary_round/submission/) and [`2_final_round/submission/`](../2_final_round/submission/).

---

## 🏁 Final Round

Team Nexora was shortlisted for the final round: a physical live pitch of 10 minutes, including the dashboard demonstration, followed by 5 minutes of Q&A. Slide decks were not required in the preliminary round. The final-round slides, dashboard and script are in [`2_final_round/`](../2_final_round/).

Marking scheme (source: [`DOSM_Datathon_2026_Final_Round_Rubric_EN.pdf`](./DOSM_Datathon_2026_Final_Round_Rubric_EN.pdf)):

| Code | Criterion | Weight |
| :--- | :--- | :---: |
| C1 PJT | Presentation & Project Mastery | 20% |
| C2 DEM | Product / Dashboard Demonstration | 25% |
| C3 ANL | Analysis Quality & Justification | 20% |
| C4 IMP | Impact, Effectiveness & Feasibility | 25% |
| C5 INV | Creativity & Innovation | 10% |

---

## 📦 Preliminary Round Submission Guide

### 1. Written Project Report (`Nexora_Datathon2026_Report.pdf`)

* **Specifications**: PDF format | Max **25 pages** (strictly excluding Front page, Table of contents, References) | **Times New Roman 12 pt** | **1.5 line spacing** | **Justified alignment** | Official DOSM cover page template.
* **Required Structure**:
  1. **Front page** *(excluded from page count)*
  2. **Table of contents** *(excluded from page count)*
  3. **Introduction**: Background, Problem statement, Research objectives
  4. **Literature review**
  5. **Methodology and data-analysis methods**
  6. **Findings**: Results, information architecture / solution approach, visual aids
  7. **Output (dashboard)**
  8. **Conclusion**
  9. **References** *(excluded from page count)*

### 2. Dashboard Package (`Nexora_Datathon2026_Dashboard.zip`)

*Local Workspace*: [`1_preliminary_round/dashboard/`](../1_preliminary_round/dashboard/)

The ZIP contains these 4 files at its root:
1. **`Dashboard.pdf`**: High-resolution static view of all completed dashboard pages.
2. **`Dashboard.pbix`** *(or `.xlsx`/`.twbx`)*: Original interactive dashboard file (fully functional filters, slicers & drill-downs; zero broken calculations; self-contained without external database dependencies).
3. **`Data.xlsx`** *(or `Data.csv`, if applicable)*: Data used by the dashboard.
4. **`README.txt`**: Plain-text document covering:
   - Software name and version used
   - Step-by-step instructions to open the dashboard
   - Navigation guide (filters, slicers, cross-filtering, views)
   - Required plugins or add-ons (if any)
   - Limitations, assumptions or special considerations

> [!NOTE]
> Static screenshots inside the written report do **not** replace the interactive dashboard file.

### 3. Video Presentation (`Nexora_Datathon2026_Video.mp4`)

* **Specifications**: **MP4** format | **Maximum 10 minutes** | Clear, professional visuals, text and audio | The dashboard shown must be fully functional, with all interactive features demonstrated.
* **Required Flow**:
  1. *Introduction of the team and project title* (within 1 minute)
  2. *Problem statement and objectives*
  3. *Data sources and methodology*
  4. *Key findings and insights*
  5. *Live demonstration of the interactive dashboard*
  6. *Conclusion and potential impact or scalability*

---

## ⚖️ Data Rules & Compliance

* **Authenticity**: Use open, publicly accessible data from credible platforms. **Fabricated, simulated or fictional data is strictly prohibited.**
* **Bonus Marks**: Extra marks for using Malaysian official data (e.g. OpenDOSM, eStatistik, StatsDW), subject to judging criteria.
* **Attribution**: Cite every external dataset, library and pre-trained model in the report and document how it was used.
* **Privacy**: No personally identifiable or confidential data without proper authorisation.
