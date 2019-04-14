SELECT Cities.city, Weather_daily_temps.date_full, Weather_daily_temps.daily_min, Weather_daily_temps.daily_avg, Weather_daily_temps.daily_max
FROM Cities JOIN Weather_daily_temps ON Cities.id = Weather_daily_temps.city_id
WHERE Weather_daily_temps.daily_max > '50'