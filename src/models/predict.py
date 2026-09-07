"""Generate predictions from a fitted model."""


def predict(model, features):
    """Return predictions for the supplied feature matrix."""
    return model.predict(features)