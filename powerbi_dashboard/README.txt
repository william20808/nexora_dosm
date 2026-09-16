==============================================================================
DOSM DATATHON 2026 - INTERACTIVE POWER BI DASHBOARD PACKAGE
Team: Nexora
Project: Malaysian Tourism Demand Forecasting & Macroeconomic Analytics
Package Archive: Nexora_Datathon2026_Dashboard.zip
==============================================================================

1. OVERVIEW & SOFTWARE REQUIREMENTS
------------------------------------------------------------------------------
- Dashboard File: Dashboard.pbix
- Application: Microsoft Power BI Desktop
- Recommended Version: September 2026 Release (or any version 2.120+ / 64-bit)
- Static Reference Deliverable: Dashboard.pdf (High-resolution multi-page PDF)
- Cleaned Underlying Data File: Data.csv (UTF-8 encoded flat dataset)
- Primary Data Sources: OpenDOSM, Bank Negara Malaysia (BNM), Ministry of
  Tourism, Arts and Culture (MOTAC), and Department of Statistics Malaysia.


2. STEP-BY-STEP: HOW TO OPEN THE DASHBOARD
------------------------------------------------------------------------------
Step 1: Ensure Microsoft Power BI Desktop is installed on your Windows machine
        (Power BI Desktop is available free from Microsoft Store / web).
Step 2: Double-click 'Dashboard.pbix', or launch Power BI Desktop and select:
        File -> Open report -> Browse reports -> select 'Dashboard.pbix'.
Step 3: The data model is pre-packaged and self-contained (Import Mode).
        When prompted, click 'Load' or 'Apply Changes'. No cloud gateway or
        enterprise credentials are required.
Step 4: (Optional) If you wish to re-point to 'Data.csv' from a different folder:
        Go to: Home -> Transform Data -> Data source settings -> Change Source,
        browse to the location of 'Data.csv', and click 'Close & Apply'.
Step 5: For quick offline review, static evaluation, or printing, open
        'Dashboard.pdf'.


3. DASHBOARD ARCHITECTURE & HOW TO NAVIGATE
------------------------------------------------------------------------------
The dashboard contains four dedicated analytical pages accessible via the left
navigation pane or page tabs along the bottom:

Page 1: Executive Overview & Tourism Recovery
  - High-level KPIs: Total Tourist Arrivals, Year-over-Year (YoY) Growth %,
    ASEAN vs. Non-ASEAN Contribution %, and Recovery Ratio vs 2019 Pre-Pandemic.
  - Interactive slicers: Filter by Year (2017 - 2026) and Month.

Page 2: Origin Market Dynamics (ASEAN vs. Non-ASEAN)
  - Drill-down across 20 international source markets (7 ASEAN, 13 Non-ASEAN).
  - Country-level ranking charts, market share breakdown, and seasonality heatmaps.
  - Cross-filtering: Click on any country bar or segment tile to cross-filter
    all charts on the page simultaneously.

Page 3: Macroeconomic & Geopolitical Drivers
  - Analysis of bilateral exchange rates (MYR per source currency).
  - Energy price indicators: Brent crude (USD/bbl) and domestic fuel (RON95/RON97).
  - Geopolitical Risk Index (GPR) trends and their correlation with arrival dips.

Page 4: Predictive Analytics & Scenario Simulator
  - Machine learning model forecasts vs. historical actuals.
  - Interactive What-If parameters: Test tourism demand response to FX changes
    and transport cost fluctuations.
  - Hold-out evaluation window projection tracking.


4. USER INTERACTION & CONTROLS
------------------------------------------------------------------------------
- Slicers: Located in the top header and filter panel (Year, Month, Market, Country).
- Interactive Cross-Filtering: Selecting any data point or bar on any visual
  dynamically highlights and filters all related visuals on that page.
- Tooltips: Hover your cursor over any data point to reveal rich contextual details,
  exact figures, percentage shares, and growth rates.
- Reset Filters: Click the 'Reset All Filters' bookmark button at the top right
  of any page to return to the default overview state.


5. REQUIRED PLUGINS, ADD-ONS & DEPENDENCIES
------------------------------------------------------------------------------
- Zero external, proprietary, or paid plugins required.
- 100% native Microsoft Power BI core visual components (Clustered Bar,
  Line & Clustered Column, Matrix, KPI Cards, Decomposition Tree, Slicers).
- Fully compliant with the Datathon competition requirement to run smoothly
  and without error on any judge's workstation.


6. ASSUMPTIONS & TECHNICAL LIMITATIONS
------------------------------------------------------------------------------
- Temporal Coverage: Spans March 2017 to September 2026.
- Observation Granularity: Monthly aggregate arrivals across 20 source countries.
- Hold-out Split: Historical observations up to the training cutoff are marked
  'Training eligible'; post-cutoff observations are reserved for scoring.
- Currency Valuation: All foreign exchange rates are bilateral averages against
  the Malaysian Ringgit (MYR) sourced from Bank Negara Malaysia (BNM).
- Imputation Transparency: Imputed indicators reflect the audited dataset with
  full metadata provenance recorded in the repository's data catalog.
==============================================================================
