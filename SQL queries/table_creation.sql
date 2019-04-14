CREATE TABLE Cities (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	city TEXT UNIQUE,
	link TEXT UNIQUE
);

CREATE TABLE Weather_daily_temps (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	city_id INTEGER,
	date_full TEXT,
	daily_min REAL,
	daily_avg REAL,
	daily_max REAL
);

CREATE TABLE Weather_monthly_temps (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	city_id INTEGER,
	date_month TEXT,
	avg_month REAL
);