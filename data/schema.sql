-- Schema for DOSM Tourism Datathon Database (dosm_datathon.db)
-- Generated from dataset.xlsx

-- TABLE: imputed_panel_data
CREATE TABLE "imputed_panel_data" (
"date" TEXT,
  "source_country_iso3" TEXT,
  "source_country_name" TEXT,
  "source_currency_code" TEXT,
  "market_segment" TEXT,
  "year" INTEGER,
  "month" INTEGER,
  "monthly_tourist_arrivals" REAL,
  "monthly_arrivals_available_flag" INTEGER,
  "monthly_myr_per_source_currency" REAL,
  "target_missing_flag" INTEGER,
  "model_row_status" TEXT
);

-- TABLE: imputed_time_series_data
CREATE TABLE "imputed_time_series_data" (
"month" TEXT,
  "year" INTEGER,
  "month_number" INTEGER,
  "gpr_global_index" REAL,
  "gpr_malaysia_index" REAL,
  "brent_crude_usd_bbl" REAL,
  "leading_index" REAL,
  "coincident_index" REAL,
  "lagging_index" REAL,
  "leading_diffusion_index" REAL,
  "coincident_diffusion_index" REAL,
  "ron95_rm_litre_monthly_avg" REAL,
  "ron97_rm_litre_monthly_avg" REAL,
  "diesel_peninsular_rm_litre_monthly_avg" REAL,
  "diesel_east_malaysia_rm_litre_monthly_avg" REAL,
  "gpr_observations_in_month" INTEGER,
  "brent_observations_in_month" INTEGER,
  "mei_observations_in_month" INTEGER,
  "fuel_source_observations_in_month" INTEGER,
  "fuel_effective_days_in_month" INTEGER,
  "period_days_in_file" INTEGER,
  "calendar_days_in_month" INTEGER,
  "fuel_coverage_pct" INTEGER,
  "period_complete_flag" INTEGER,
  "fuel_low_coverage_flag" INTEGER,
  "retrieved_at_utc" REAL,
  "gpr_global_index_imputed_flag" INTEGER,
  "gpr_malaysia_index_imputed_flag" INTEGER,
  "brent_crude_usd_bbl_imputed_flag" INTEGER,
  "leading_index_imputed_flag" INTEGER,
  "coincident_index_imputed_flag" INTEGER,
  "lagging_index_imputed_flag" INTEGER,
  "leading_diffusion_index_imputed_flag" INTEGER,
  "coincident_diffusion_index_imputed_flag" INTEGER,
  "imputed_predictor_count" INTEGER,
  "any_predictor_imputed_flag" INTEGER,
  "imputation_status" TEXT
);

-- TABLE: original_panel_data
CREATE TABLE "original_panel_data" (
"date" TEXT,
  "source_country_iso3" TEXT,
  "source_country_name" TEXT,
  "source_currency_code" TEXT,
  "market_segment" TEXT,
  "year" INTEGER,
  "month" INTEGER,
  "monthly_tourist_arrivals" REAL,
  "monthly_arrivals_available_flag" INTEGER,
  "monthly_myr_per_source_currency" REAL
);

-- TABLE: original_time_series_data
CREATE TABLE "original_time_series_data" (
"month" TEXT,
  "year" INTEGER,
  "month_number" INTEGER,
  "gpr_global_index" REAL,
  "gpr_malaysia_index" REAL,
  "brent_crude_usd_bbl" REAL,
  "leading_index" REAL,
  "coincident_index" REAL,
  "lagging_index" REAL,
  "leading_diffusion_index" REAL,
  "coincident_diffusion_index" REAL,
  "ron95_rm_litre_monthly_avg" REAL,
  "ron97_rm_litre_monthly_avg" REAL,
  "diesel_peninsular_rm_litre_monthly_avg" REAL,
  "diesel_east_malaysia_rm_litre_monthly_avg" REAL,
  "gpr_observations_in_month" INTEGER,
  "brent_observations_in_month" INTEGER,
  "mei_observations_in_month" INTEGER,
  "fuel_source_observations_in_month" INTEGER,
  "fuel_effective_days_in_month" INTEGER,
  "period_days_in_file" INTEGER,
  "calendar_days_in_month" INTEGER,
  "fuel_coverage_pct" INTEGER,
  "period_complete_flag" INTEGER,
  "fuel_low_coverage_flag" INTEGER,
  "retrieved_at_utc" REAL
);

-- INDEX: idx_ipd_country_date
CREATE INDEX [idx_ipd_country_date] ON [imputed_panel_data] ([source_country_iso3], [date]);

-- INDEX: idx_ipd_country_year_month
CREATE INDEX [idx_ipd_country_year_month] ON [imputed_panel_data] ([source_country_iso3], [year], [month]);

-- INDEX: idx_its_month
CREATE INDEX [idx_its_month] ON [imputed_time_series_data] ([month]);

-- INDEX: idx_its_year_month
CREATE INDEX [idx_its_year_month] ON [imputed_time_series_data] ([year], [month_number]);

-- INDEX: idx_opd_country_date
CREATE INDEX [idx_opd_country_date] ON [original_panel_data] ([source_country_iso3], [date]);

-- INDEX: idx_opd_country_year_month
CREATE INDEX [idx_opd_country_year_month] ON [original_panel_data] ([source_country_iso3], [year], [month]);

-- INDEX: idx_ots_month
CREATE INDEX [idx_ots_month] ON [original_time_series_data] ([month]);

-- INDEX: idx_ots_year_month
CREATE INDEX [idx_ots_year_month] ON [original_time_series_data] ([year], [month_number]);

-- TABLE: sources
CREATE TABLE "sources" (
  "workbook_sheet" TEXT,
  "variable_code" TEXT,
  "variable_name" TEXT,
  "what_it_comes_from" TEXT,
  "original_source_field_or_formula" TEXT,
  "release_agency" TEXT,
  "source_dataset_or_series" TEXT,
  "api_or_download_url_used" TEXT,
  "access_method" TEXT,
  "source_classification" TEXT,
  "frequency" TEXT,
  "measurement_unit" TEXT,
  "cleaning_or_derivation_applied" TEXT,
  "original_missing_count" INTEGER,
  "original_missing_rate_pct" REAL,
  "final_missing_count" INTEGER,
  "related_flag_or_important_note" TEXT
);

-- INDEX: idx_sources_sheet_var
CREATE INDEX [idx_sources_sheet_var] ON [sources] ([workbook_sheet], [variable_code]);

