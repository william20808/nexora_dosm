UPDATE athlete_training
SET gender = NULLIF(TRIM(gender), ''),
    training_type = NULLIF(TRIM(training_type), '');

DELETE FROM athlete_training
WHERE athlete_id IS NULL OR TRIM(athlete_id) = '';