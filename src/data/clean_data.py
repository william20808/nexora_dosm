"""Apply lightweight, deterministic cleaning to a CSV dataset."""

from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


def clean_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and remove fully empty rows and columns."""
    cleaned = frame.dropna(axis=0, how="all").dropna(axis=1, how="all").copy()
    cleaned.columns = [
        str(column).strip().lower().replace(" ", "_") for column in cleaned.columns
    ]
    return cleaned


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input_path")
    parser.add_argument("--output", default="database/clean_data.csv")
    arguments = parser.parse_args()
    cleaned = clean_frame(pd.read_csv(arguments.input_path))
    destination = Path(arguments.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(destination, index=False)
    print(f"Wrote {len(cleaned)} rows into {arguments.output}")


if __name__ == "__main__":
    main()