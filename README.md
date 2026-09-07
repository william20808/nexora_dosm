# nexora_dosm
Competition of DOSM code and documents

nexora_dosm/
├── README.md
├── requirements.txt
├── .gitignore
│
├── database/
│   ├── dosm_datathon.db
│   ├── schema.sql
│   ├── cleaning.sql
│   └── queries.sql
│
├── src/
│   ├── data/
│   │   ├── import_data.py
│   │   └── clean_data.py
│   ├── features/
│   │   └── feature_engineering.py
│   ├── models/
│   │   ├── train.py
│   │   └── predict.py
│   └── evaluation/
│       ├── evaluate.py
│       └── explainability.py
│
└── dashboard/
    ├── Dashboard.pbix
    ├── Dashboard.pdf
    ├── Data.csv
    └── README.txt
