"""Build numeric model features from cleaned tabular data."""

import pandas as pd


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Return numeric columns with missing values filled by their medians."""
    numeric = frame.select_dtypes(include="number").copy()
    return numeric.fillna(numeric.median(numeric_only=True))