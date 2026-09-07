SELECT training_type,
       COUNT(*) AS athlete_count,
       AVG(performance_score) AS average_performance,
       AVG(injury_risk) AS average_injury_risk
FROM athlete_training
GROUP BY training_type
ORDER BY athlete_count DESC;

SELECT gender,
       AVG(training_frequency) AS average_training_frequency,
       AVG(training_duration_minutes) AS average_duration_minutes
FROM athlete_training
GROUP BY gender
ORDER BY gender;