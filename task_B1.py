# PART B - TASK B1: Implement and Validate the Cleaning Pipeline & SQLite Storage
import csv
import io
import sqlite3

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Velachery,2026-10-04,1500
"""


def load_clean(text):
    """Returns (station, date, pm25) tuples for valid, non-negative, and <= 999 readings only."""
    rows = []
    f = io.StringIO(text.strip())
    reader = csv.DictReader(f)
    for r in reader:
        raw_pm = r["pm25"].strip()
        if not raw_pm or raw_pm == "NA":
            continue
        try:
            pm_val = float(raw_pm)
            if pm_val < 0 or pm_val > 999:
                continue
            rows.append((r["station"].strip(), r["date"].strip(), pm_val))
        except ValueError:
            continue
    return rows


def min_max(values):
    """Scale each value to 0-1 range, rounded to 3 decimals."""
    if not values:
        return []
    min_v = min(values)
    max_v = max(values)
    if max_v == min_v:
        return [0.0 for _ in values]
    return [round((v - min_v) / (max_v - min_v), 3) for v in values]


if __name__ == "__main__":
    clean = load_clean(RAW)
    print("Cleaned Records:", clean)
    print("Min-Max Scaled:", min_max([pm for _, _, pm in clean]))

    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
    cleaned_data = [
        ("Adyar", "2026-10-01", 48.0),
        ("Guindy", "2026-10-01", 95.0),
        ("Guindy", "2026-10-03", 121.0),
        ("Adyar", "2026-10-04", 60.0),
    ]
    cur.executemany("INSERT INTO aq VALUES (?, ?, ?)", cleaned_data)
    con.commit()

    cur.execute("SELECT AVG(pm25) FROM aq WHERE station='Adyar'")
    avg_adyar = cur.fetchone()[0]
    print(f"Adyar Average PM2.5: {avg_adyar:.2f}")
    con.close()
