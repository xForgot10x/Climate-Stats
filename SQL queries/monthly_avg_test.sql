select avg (Weather_monthly_temps.avg_month)
from Weather_monthly_temps join Cities
on Weather_monthly_temps.city_id = Cities.id
where Cities.city = 'Ufa' and strftime ('%Y', Weather_monthly_temps.date_month) = '2019'