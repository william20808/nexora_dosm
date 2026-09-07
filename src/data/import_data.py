"""Import a source CSV into a normalized CSV artifact."""

from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


def import_csv(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    """Read a CSV and write it to the requested output location."""
    frame = pd.read_csv(input_path)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination, index=False)
    return frame


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input_path")
    parser.add_argument("--output", default="database/raw_data.csv")
    arguments = parser.parse_args()
    imported = import_csv(arguments.input_path, arguments.output)
    print(f"Imported {len(imported)} rows into {arguments.output}")


if __name__ == "__main__":
    main()