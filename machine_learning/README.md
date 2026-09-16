# 🤖 Machine Learning Pipeline

This directory contains the machine learning codebase and modular scripts for Team **Nexora** in the DOSM Datathon 2026.

It is structured into dedicated modules for feature engineering, model training, hold-out prediction, and performance evaluation:

---

## 📁 Directory Structure

```text
machine_learning/
├── README.md                      # Machine learning architecture documentation
├── features/
│   └── feature_engineering.py     # Feature extraction, lag generation, and data transformations
├── models/
│   ├── train.py                   # Model training, validation, and hyperparameter tuning
│   └── predict.py                 # Prediction generation for the hold-out evaluation dataset
└── evaluation/
    ├── evaluate.py                # Model scoring and error metrics (MAPE, RMSE, MAE)
    └── explainability.py          # Feature importance, attribution, and sensitivity analysis
```

---

## ⚙️ Module Overview

- **`features/`**: Handles loading datasets from `data/dosm_datathon.db`, constructing temporal lag variables, rolling statistics, and integrating macroeconomic and foreign exchange predictors.
- **`models/`**: Contains routines for training predictive models on historical training data and generating tourist arrival forecasts for the unlabelled hold-out period.
- **`evaluation/`**: Provides functions to assess model accuracy against validation sets and compute feature attribution to support findings in the project report.
