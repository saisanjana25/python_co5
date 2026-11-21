# PART A - TASK A3: Design the Analysis and Visualisation (Daily Station Summary Query)
import sqlite3

SUMMARY_QUERY = """
SELECT
    s.station_name,
    r.reading_date,
    MIN(r.pm25) AS min_pm25,
    MAX(r.pm25) AS max_pm25,
    ROUND(AVG(r.pm25), 2) AS mean_pm25,
    COUNT(r.pm25) AS valid_readings_count
FROM readings r
JOIN stations s ON r.station_id = s.station_id
GROUP BY s.station_name, r.reading_date;
"""


if __name__ == "__main__":
    con = sqlite3.connect(":memory:")
    con.executescript(
        """
        CREATE TABLE stations (station_id INTEGER PRIMARY KEY, station_name TEXT);
        CREATE TABLE readings (station_id INTEGER, reading_date TEXT, pm25 REAL);
        INSERT INTO stations VALUES (1, 'Adyar'), (2, 'Guindy');
        INSERT INTO readings VALUES
            (1, '2026-10-01', 42.0),
            (1, '2026-10-01', 54.0),
            (2, '2026-10-01', 95.0);
        """
    )
    for row in con.execute(SUMMARY_QUERY):
        print(row)
    con.close()
