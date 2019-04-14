import re
from datetime import date
import sqlite3
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

def win_safe_name(cityname):
    """Edit the string so that it can be used as a valid file name in
    Windows.
    """
    cityname = cityname.strip()
    if cityname.endswith("."):
        cityname = cityname[:-1] + "_"
    for chr in cityname:
        if chr in ("<", ">", ":", "/", "\\", "|", "?", "*", "\""):
            cityname = cityname.replace(chr, "_")
    return cityname

# Database connection
conn = sqlite3.connect("weather_data.sqlite3")
cur = conn.cursor()

# User input and sanity checks
city = input("Enter the city name: ")
city = win_safe_name(city)
logfile = city + "_log.txt"
base_url = input("Link to the climate monitor: ")
if not base_url.startswith("http://www.pogodaiklimat.ru/monitor"):
    print("Wrong URL format")
    conn.close()
    quit()
# Put this data into Cities table
cur.execute("INSERT INTO Cities (city, link) VALUES (?, ?)", (city, base_url))
# Prepare the URL for parsing afterwards
base_url = base_url + "&"
# Retrieve id from Cities table for later use
cur.execute("SELECT id FROM Cities WHERE city = ?", (city,))
city_id = cur.fetchone()[0]

# Iterate through all pages for years 2001-2018, all months
for year in range(2001, 2019):
    print("Processing year:", year)
    for month in range(1, 13):
        # Get a link, try to open it.  Handle failures
        dest_url = (base_url
                    + urllib.parse.urlencode({"month": month, "year": year}))
        try:
            uh = urllib.request.urlopen(dest_url)
        except:
            print("Could not open", dest_url)
            print("Exiting")
            conn.close()
            with open(logfile, "a+") as f:
                f.write(F"Could not open {dest_url}\n")
            quit()
        # Parse the page
        soup = BeautifulSoup(uh, "html.parser")
        # Get monthly average temperature directly from the page
        try:
            avg_month = re.findall("наблюдений: (\S+)°", soup.get_text())[0]
            avg_month = float(avg_month)
        except:
            # If there is no data, put None into the variable
            avg_month = None
            print("Incorrect data for:", year, month)
            with open(logfile, "a+") as f:
                f.write(F"Incorrect monthly average for: {year} {month}\n")
        # Use 1st day of the month for dates.  datetime.date for
        # constructing the date, which is converted into string
        date_month = str(date(year, month, 1))
        # Put data into Weather_monthly_temps
        cur.execute("""INSERT INTO Weather_monthly_temps
                    (city_id, date_month, avg_month)
                    VALUES (?, ?, ?)""", (city_id, date_month, avg_month))

        # Table parsing.  We need a table nested inside the second one.
        table = soup.find_all("table")[2]
        # The first two rows contain column descriptions
        table_rows = table.find_all("tr")[2:]
        # tr for "table row" and td for "table data"
        for tr in table_rows:
            # Get day number for date construction
            day = int(tr.find("th").text)
            # Sanity check as tables always have 29 days for February
            try:
                date_full = str(date(year, month, day))
            except:
                continue
            td = tr.find_all("td")
            # Get text values from "td" tags
            row = [item.text for item in td]
            # Put these values into variables for readability.  Set
            # missing data to None
            try:
                daily_min = float(row[0])
                daily_avg = float(row[1])
                daily_max = float(row[2])
            except:
                daily_min = None
                daily_avg = None
                daily_max = None
            # Put data into Weather_daily_temps
            cur.execute("""INSERT INTO Weather_daily_temps
                        (city_id, date_full, daily_min, daily_avg, daily_max)
                        VALUES (?, ?, ?, ?, ?)""",
                        (city_id, date_full, daily_min, daily_avg, daily_max))
    # Make sure to commit after every month
    conn.commit()

uh.close()
conn.close()
print("Done parsing data for", city)
