# nexora_dosm

Data preparation, modelling, evaluation, and dashboard assets for the DOSM datathon.

## Project layout

- `database/`: SQLite schema, cleaning statements, and analysis queries.
- `src/`: import, cleaning, feature engineering, modelling, and evaluation modules.
- `dashboard/`: dashboard handover notes and exported assets.

## Quick start

```text
pip install -r requirements.txt
python -m src.data.import_data path/to/data.csv --output database/raw_data.csv
python -m src.data.clean_data database/raw_data.csv --output database/clean_data.csv
```

The pipeline accepts a CSV file and preserves the original columns while applying
standard column-name normalization and missing-value handling.
