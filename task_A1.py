# PART A - TASK A1: Design the Data Acquisition (SQLite Schema & Query Setup)
import sqlite3

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS stations (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_name TEXT NOT NULL UNIQUE,
    location_zone TEXT NOT NULL,
    latitude REAL,
    longitude REAL
);

CREATE TABLE IF NOT EXISTS readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INTEGER NOT NULL,
    reading_date TEXT NOT NULL,
    reading_hour INTEGER NOT NULL CHECK (reading_hour >= 0 AND reading_hour <= 23),
    pm25 REAL CHECK (pm25 >= 0 AND pm25 <= 1000),
    pm10 REAL CHECK (pm10 >= 0 AND pm10 <= 2000),
    no2 REAL CHECK (no2 >= 0 AND no2 <= 1000),
    temperature_c REAL CHECK (temperature_c >= -10 AND temperature_c <= 60),
    FOREIGN KEY (station_id) REFERENCES stations(station_id),
    UNIQUE(station_id, reading_date, reading_hour)
);

CREATE INDEX IF NOT EXISTS idx_station_date ON readings(station_id, reading_date);
"""


def init_db(db_path=":memory:"):
    con = sqlite3.connect(db_path)
    con.executescript(SCHEMA_SQL)
    return con


if __name__ == "__main__":
    conn = init_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO stations (station_name, location_zone, latitude, longitude) VALUES (?, ?, ?, ?)",
        ("Adyar", "South", 13.0012, 80.2565),
    )
    cur.execute(
        """
        INSERT INTO readings (station_id, reading_date, reading_hour, pm25, pm10, no2, temperature_c)
        VALUES (1, '2026-10-01', 10, 48.0, 85.0, 30.0, 27.5)
        """
    )
    conn.commit()
    cur.execute("SELECT AVG(pm25) FROM readings WHERE station_id = 1 AND reading_date LIKE '2026-10%'")
    print("Adyar Oct 2026 Avg PM2.5:", cur.fetchone()[0])
    conn.close()
