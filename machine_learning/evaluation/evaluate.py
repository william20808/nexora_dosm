"""
machine_learning/evaluation/evaluate.py

Rolling-origin, availability-aware backtest for all four candidate models
(Naive-last, Seasonal-naive, Ridge+GPRxCountry, LightGBM), across both lag
assumptions and both fold sets (primary / COVID stress). Writes:

  outputs/backtest_accuracy_by_horizon.csv   MAE/RMSE per model x horizon x L x fold_set
  outputs/backtest_predictions.csv           out-of-sample actual-vs-predicted points (LightGBM, primary)
  outputs/covid_stress_test_summary.csv      stress-fold subset
  outputs/L3_vs_L4_sensitivity_summary.csv   lag-assumption robustness

Metrics are MAE and RMSE (per lecturer guidance). Reported PER HORIZON, never
pooled into a single number.

Run:  python -m machine_learning.evaluation.evaluate
"""

import warnings; warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

from .. import config
from ..features.feature_engineering import build_horizon_table, make_backtest_fold


def _lgbm(train, val):
    feats = config.FINAL_FEATURES + [config.CATEGORICAL_FEATURE]
    Xtr, Xva = train[feats].copy(), val[feats].copy()
    Xtr[config.CATEGORICAL_FEATURE] = Xtr[config.CATEGORICAL_FEATURE].astype("category")
    Xva[config.CATEGORICAL_FEATURE] = (Xva[config.CATEGORICAL_FEATURE].astype("category")
                                       .cat.set_categories(Xtr[config.CATEGORICAL_FEATURE].cat.categories))
    m = lgb.LGBMRegressor(**config.LGBM_PARAMS)
    m.fit(Xtr, train["target_arrivals"], categorical_feature=[config.CATEGORICAL_FEATURE])
    return np.clip(m.predict(Xva), 0, None)


def _ridge(train, val, countries):
    ref = config.RIDGE_REFERENCE_COUNTRY
    non_ref = [c for c in countries if c != ref]

    def make_X(df, cols=None):
        X = df[config.FINAL_FEATURES].copy()
        for c in non_ref:
            X[f"gpr_x_{c}"] = df["gpr_global_index"] * (df["source_country_iso3"] == c).astype(int)
        cd = pd.get_dummies(df["source_country_iso3"], prefix="c")
        cd = cd[[f"c_{c}" for c in non_ref if f"c_{c}" in cd.columns]]
        X = pd.concat([X.reset_index(drop=True), cd.reset_index(drop=True)], axis=1)
        return X.reindex(columns=cols, fill_value=0) if cols is not None else X

    Xtr = make_X(train); Xva = make_X(val, Xtr.columns)
    med = Xtr.median(numeric_only=True); Xtr = Xtr.fillna(med); Xva = Xva.fillna(med)
    sc = StandardScaler(); Xtr_s = sc.fit_transform(Xtr); Xva_s = sc.transform(Xva)
    m = Ridge(alpha=config.RIDGE_ALPHA).fit(Xtr_s, train["target_arrivals"])
    return np.clip(m.predict(Xva_s), 0, None)


def _evaluate(L, folds, label, keep_predictions=False):
    table = build_horizon_table(L_arrivals=L)
    countries = sorted(table["source_country_iso3"].unique())
    recs, preds = [], []
    for vo in folds:
        train, val = make_backtest_fold(table, vo)
        if len(val) == 0 or len(train) < 100:
            continue
        model_preds = {
            "Naive-last": val["origin_arrivals"].values,
            "Seasonal-naive": val["seasonal_naive_target"].fillna(val["origin_arrivals"]).values,
            "Ridge_GPRxCountry": _ridge(train, val, countries),
            "LightGBM": _lgbm(train, val),
        }
        actual = val["target_arrivals"].values
        for h in sorted(val["horizon"].unique()):
            msk = (val["horizon"] == h).values
            for name, p in model_preds.items():
                err = actual[msk] - p[msk]
                recs.append(dict(L_arrivals=L, fold_set=label, horizon=h, model=name,
                                 mae=np.mean(np.abs(err)), rmse=np.sqrt(np.mean(err ** 2)), n=msk.sum()))
        if keep_predictions:
            tmp = val[["source_country_iso3", "source_country_name", "market_segment",
                       "target_period", "horizon", "target_arrivals"]].copy()
            tmp["predicted_arrivals"] = model_preds["LightGBM"].round(0)
            tmp["fold_origin"] = pd.Timestamp(vo).strftime("%Y-%m-01")
            preds.append(tmp)
    return pd.DataFrame(recs), (pd.concat(preds, ignore_index=True) if preds else pd.DataFrame())


def run_all():
    frames, bt_pred = [], pd.DataFrame()
    for L in (config.L_ARRIVALS_PRIMARY, config.L_ARRIVALS_SENSITIVITY):
        p, pred = _evaluate(L, config.PRIMARY_FOLDS, "primary",
                            keep_predictions=(L == config.L_ARRIVALS_PRIMARY))
        s, _ = _evaluate(L, config.STRESS_FOLDS, "stress_covid")
        frames += [p, s]
        if L == config.L_ARRIVALS_PRIMARY:
            bt_pred = pred
    raw = pd.concat(frames, ignore_index=True)
    summary = (raw.groupby(["L_arrivals", "fold_set", "horizon", "model"])
               .apply(lambda g: pd.Series({"MAE": np.average(g["mae"], weights=g["n"]),
                                           "RMSE": np.sqrt(np.average(g["rmse"] ** 2, weights=g["n"]))}))
               .reset_index())

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(config.OUTPUT_DIR / "backtest_accuracy_by_horizon.csv", index=False)

    if not bt_pred.empty:
        bt_pred = bt_pred.rename(columns={"target_period": "period", "target_arrivals": "actual_arrivals"})
        bt_pred["period"] = bt_pred["period"].dt.strftime("%Y-%m-01")
        bt_pred["split_type"] = "backtest_out_of_sample"
        bt_pred.to_csv(config.OUTPUT_DIR / "backtest_predictions.csv", index=False)

    summary[summary["fold_set"] == "stress_covid"].to_csv(
        config.OUTPUT_DIR / "covid_stress_test_summary.csv", index=False)

    sens = summary[(summary["fold_set"] == "primary") &
                   (summary["model"].isin(["LightGBM", "Naive-last", "Seasonal-naive"]))]
    sens_wide = sens.pivot_table(index=["horizon", "model"], columns="L_arrivals", values="MAE").reset_index()
    sens_wide.columns = ["horizon", "model", "MAE_L3", "MAE_L4"]
    sens_wide["pct_diff_L3_vs_L4"] = (100 * (sens_wide["MAE_L3"] - sens_wide["MAE_L4"]) / sens_wide["MAE_L4"]).round(1)
    sens_wide.to_csv(config.OUTPUT_DIR / "L3_vs_L4_sensitivity_summary.csv", index=False)

    print("Wrote: backtest_accuracy_by_horizon, backtest_predictions, "
          "covid_stress_test_summary, L3_vs_L4_sensitivity_summary")
    return summary


if __name__ == "__main__":
    run_all()
