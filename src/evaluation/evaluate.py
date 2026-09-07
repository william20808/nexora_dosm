"""Metrics for regression model evaluation."""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_regression(actual, predicted):
    """Return common regression metrics."""
    return {
        "mae": mean_absolute_error(actual, predicted),
        "rmse": mean_squared_error(actual, predicted) ** 0.5,
        "r2": r2_score(actual, predicted),
    }