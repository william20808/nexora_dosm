"""Train a baseline regression model."""

from sklearn.ensemble import RandomForestRegressor


def train_model(features, target):
    """Fit and return a reproducible baseline random forest."""
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    return model.fit(features, target)