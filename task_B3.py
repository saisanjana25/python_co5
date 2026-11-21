# PART B - TASK B3: Loops vs Libraries vs SQL Correctness Verification
import sqlite3
import pandas as pd

data = [
    ("Adyar", "2026-10-01", 48.0),
    ("Guindy", "2026-10-01", 95.0),
    ("Guindy", "2026-10-03", 121.0),
    ("Adyar", "2026-10-04", 60.0),
]

# Method 1: Plain Python Loops
sum_pm = 0.0
count = 0
for s, d, pm in data:
    if s == "Adyar":
        sum_pm += pm
        count += 1
mean_loop = sum_pm / count

# Method 2: Pandas Groupby
df = pd.DataFrame(data, columns=["station", "day", "pm25"])
mean_pandas = df[df["station"] == "Adyar"]["pm25"].mean()

# Method 3: SQL GROUP BY
con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
cur.executemany("INSERT INTO aq VALUES (?, ?, ?)", data)
cur.execute("SELECT AVG(pm25) FROM aq WHERE station='Adyar'")
mean_sql = cur.fetchone()[0]
con.close()

assert mean_loop == mean_pandas == mean_sql == 54.00
print(f"Loop: {mean_loop:.2f} | Pandas: {mean_pandas:.2f} | SQL: {mean_sql:.2f}")
