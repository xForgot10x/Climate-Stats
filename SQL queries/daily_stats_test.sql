SELECT COUNT (Weather_daily_temps.daily_min)
FROM Weather_daily_temps JOIN Cities
ON Weather_daily_temps.city_id = Cities.id
WHERE Weather_daily_temps.daily_min < '0' and Cities.city = 'Moscow'