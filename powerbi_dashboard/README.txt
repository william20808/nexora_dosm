================================================================================
TEAM NEXORA - DOSM DATATHON 2026
INTERACTIVE DASHBOARD USER GUIDE & SPECIFICATIONS
================================================================================

1. SOFTWARE NAME AND VERSION
----------------------------
* Software: Microsoft Power BI Desktop
* Minimum Recommended Version: September 2026 release (Version 2.133+ or any recent build)
* Compatibility: Standard 64-bit Windows installation of Power BI Desktop

2. STEP-BY-STEP INSTRUCTIONS TO OPEN THE DASHBOARD
--------------------------------------------------
Step 1: Unzip "Nexora_Datathon2026_Dashboard.zip" into a local directory.
Step 2: Ensure "Data.csv" and "Dashboard.pbix" reside in the same folder.
Step 3: Double-click "Dashboard.pbix" to open the interactive report in 
        Microsoft Power BI Desktop.
Step 4: If Power BI prompts for data refresh or file path confirmation, navigate
        to Home > Transform Data > Data Source Settings, select "Data.csv" 
        from the local folder, and click "Apply Changes".
Step 5: Alternatively, view "Dashboard.pdf" for a high-resolution, static 
        view of all completed dashboard canvas pages.

3. USER NAVIGATION GUIDE
------------------------
* Slicers & Filters: Use top and left navigation panels to slice arrivals 
  by Source Country (20 international markets), Market Segment (ASEAN vs. 
  Non-ASEAN), Malaysian State (16 states/territories), and observation timeline (2017 to 2026).
* Cross-Filtering: Clicking any visual element (bar, map bubble, line point) 
  will dynamically cross-filter all linked charts across the canvas.
* Tooltips: Hover over any data point to display granular monthly metrics, 
  bilateral exchange rates (MYR/FX), fuel prices, geopolitical risk indices, 
  and state hotel occupancy / domestic visitor statistics.
* Reset: Click the "Reset Filters" bookmark button located at the top-right 
  of any page to return to default views.

4. REQUIRED PLUGINS OR ADD-ONS
------------------------------
* Required Add-ons: None (0 external dependencies).
* Visual Libraries: All visuals are 100% native out-of-the-box Power BI charts 
  (Native Line Charts, Clustered Column Charts, Matrix, Treemaps, and Azure Map 
  visuals). No custom marketplace visuals or unverified third-party scripts are 
  required.

5. ASSUMPTIONS AND LIMITATIONS
------------------------------
* Data Coverage: Monthly panel from March 2017 to September 2026 for international 
  tourist arrivals; annual state-level hotel occupancy and domestic visitor panel 
  from 2017 to 2025 across 16 Malaysian states and federal territories.
* Forecasting Horizon: October 2024 to September 2026 represents the official 
  hold-out evaluation period where arrival figures are predicted using the 
  machine learning models.
* Currency Rates: Bilateral exchange rates represent monthly averages published 
  by Bank Negara Malaysia (BNM).
* Geopolitical Risk: GPR indices represent Caldara & Iacoviello monthly benchmark 
  indices.
* Offline Self-Containment: The data model is completely embedded in the .PBIX 
  file cache and requires no active live database connection to operate.
================================================================================
