"""
machine_learning/evaluation/explainability.py

Interpretation outputs (NONE of these are causal -- see caveats in the data
dictionary and report):

  outputs/lightgbm_feature_importance.csv        split-count importance
  outputs/gpr_country_ridge_interaction.csv      Ridge GPR x country (USA-referenced, identifiable)
  outputs/shap_gpr_contribution_by_country.csv   mean |SHAP| of GPR features, raw + volume-normalized

Run:  python -m machine_learning.evaluation.explainability
"""

import warnings; warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import joblib
import shap
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

from .. import config
from ..features.feature_engineering import build_horizon_table, split_train_and_live


def _train_frame():
    table = build_horizon_table(L_arrivals=config.L_ARRIVALS_PRIMARY)
    train, _ = split_train_and_live(table)
    return train


def feature_importance(train):
    art = joblib.load(config.ARTIFACT_DIR / "lightgbm_final.joblib")
    model = art["model"]
    feats = art["features"] + [config.CATEGORICAL_FEATURE]
    imp = pd.Series(model.feature_importances_, index=feats).sort_values(ascending=False)
    out = imp.reset_index(); out.columns = ["feature", "importance"]
    out.to_csv(config.OUTPUT_DIR / "lightgbm_feature_importance.csv", index=False)
    return out


def ridge_gpr_by_country(train):
    ref = config.RIDGE_REFERENCE_COUNTRY
    countries = sorted(train["source_country_iso3"].unique())
    non_ref = [c for c in countries if c != ref]
    X = train[config.FINAL_FEATURES].copy()
    for c in non_ref:
        X[f"gpr_x_{c}"] = train["gpr_global_index"] * (train["source_country_iso3"] == c).astype(int)
    cd = pd.get_dummies(train["source_country_iso3"], prefix="c")[[f"c_{c}" for c in non_ref]]
    X = pd.concat([X.reset_index(drop=True), cd.reset_index(drop=True)], axis=1)
    X = X.fillna(X.median(numeric_only=True))
    Xs = StandardScaler().fit_transform(X)
    m = Ridge(alpha=config.RIDGE_ALPHA).fit(Xs, train["target_arrivals"])
    coef = pd.Series(m.coef_, index=X.columns)
    base = coef["gpr_global_index"]
    rows = []
    for c in countries:
        inter = 0.0 if c == ref else coef.get(f"gpr_x_{c}", 0.0)
        seg = train.loc[train["source_country_iso3"] == c, "market_segment"].iloc[0]
        rows.append((c, seg, inter, base + inter))
    out = pd.DataFrame(rows, columns=["source_country_iso3", "market_segment",
                                      "gpr_interaction_vs_USA", "total_standardized_gpr_slope"])
    out.to_csv(config.OUTPUT_DIR / "gpr_country_ridge_interaction.csv", index=False)
    return out


def shap_gpr_by_country(train):
    art = joblib.load(config.ARTIFACT_DIR / "lightgbm_final.joblib")
    model = art["model"]
    feats = art["features"] + [config.CATEGORICAL_FEATURE]
    X = train[feats].copy()
    X[config.CATEGORICAL_FEATURE] = (X[config.CATEGORICAL_FEATURE].astype("category")
                                     .cat.set_categories(art["category_levels"]))
    sv = pd.DataFrame(shap.TreeExplainer(model).shap_values(X), columns=feats)
    sv["source_country_iso3"] = train["source_country_iso3"].values
    sv["origin_arrivals"] = train["origin_arrivals"].values
    g = sv.groupby("source_country_iso3").apply(lambda d: pd.Series({
        "mean_abs_shap_gpr_global": d["gpr_global_index"].abs().mean(),
        "mean_abs_shap_gpr_malaysia": d["gpr_malaysia_index"].abs().mean(),
        "mean_arrival_volume": d["origin_arrivals"].mean(),
    })).reset_index()
    g["gpr_global_contribution_normalized_pct"] = 100 * g["mean_abs_shap_gpr_global"] / g["mean_arrival_volume"]
    g["gpr_malaysia_contribution_normalized_pct"] = 100 * g["mean_abs_shap_gpr_malaysia"] / g["mean_arrival_volume"]
    seg = train.groupby("source_country_iso3")["market_segment"].first().reset_index()
    g = g.merge(seg, on="source_country_iso3")
    g.to_csv(config.OUTPUT_DIR / "shap_gpr_contribution_by_country.csv", index=False)
    return g


def run_all():
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    train = _train_frame()
    feature_importance(train)
    ridge_gpr_by_country(train)
    shap_gpr_by_country(train)
    print("Wrote: lightgbm_feature_importance, gpr_country_ridge_interaction, "
          "shap_gpr_contribution_by_country")


if __name__ == "__main__":
    run_all()
