"""
machine_learning/models/train.py

Trains the final, locked model: a single pooled LightGBM (direct multi-horizon,
19 features + source_country_iso3 categorical) on ALL available history, and
persists it to artifacts/ so predict.py can load it without retraining.

Run:  python -m machine_learning.models.train
"""

import joblib
import lightgbm as lgb

from .. import config
from ..features.feature_engineering import build_horizon_table, split_train_and_live


def train_final_model(prefer_db=True, L_arrivals=None):
    L_arrivals = L_arrivals or config.L_ARRIVALS_PRIMARY
    table = build_horizon_table(prefer_db=prefer_db, L_arrivals=L_arrivals)
    train, _ = split_train_and_live(table)

    feats = config.FINAL_FEATURES + [config.CATEGORICAL_FEATURE]
    X = train[feats].copy()
    X[config.CATEGORICAL_FEATURE] = X[config.CATEGORICAL_FEATURE].astype("category")
    y = train["target_arrivals"]

    model = lgb.LGBMRegressor(**config.LGBM_PARAMS)
    model.fit(X, y, categorical_feature=[config.CATEGORICAL_FEATURE])

    config.ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    artifact = {
        "model": model,
        "features": config.FINAL_FEATURES,
        "categorical_feature": config.CATEGORICAL_FEATURE,
        "category_levels": list(X[config.CATEGORICAL_FEATURE].cat.categories),
        "L_arrivals": L_arrivals,
        "lgbm_params": config.LGBM_PARAMS,
        "n_train_rows": len(train),
    }
    path = config.ARTIFACT_DIR / "lightgbm_final.joblib"
    joblib.dump(artifact, path)
    print(f"Trained on {len(train)} rows. Saved artifact -> {path}")
    return artifact


if __name__ == "__main__":
    train_final_model()
