"""Simple model explainability helpers."""


def feature_importance(model, feature_names):
    """Pair tree-model importances with their feature names."""
    return sorted(
        zip(feature_names, model.feature_importances_),
        key=lambda item: item[1],
        reverse=True,
    )