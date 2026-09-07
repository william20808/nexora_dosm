PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS athlete_training (
    athlete_id TEXT PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    training_type TEXT,
    training_frequency REAL,
    training_duration_minutes REAL,
    performance_score REAL,
    injury_risk REAL,
    recorded_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_training_type
    ON athlete_training (training_type);