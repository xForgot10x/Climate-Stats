UPDATE Weather_daily_temps
SET daily_min = NULL, daily_avg = NULL, daily_max = NULL
WHERE city_id = 62 AND daily_max > 40 AND daily_min = 0.0