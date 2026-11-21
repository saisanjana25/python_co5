# PART A - TASK A2: Design the Cleaning and Normalisation (Cleaning, Imputation & Scaling Rules)


def clean_temperature_c(temp, is_fahrenheit=False):
    """Convert Fahrenheit to Celsius if needed or if ambient reading exceeds 45 C."""
    if temp is None:
        return None
    if is_fahrenheit or temp > 45.0:
        return round((temp - 32.0) * 5.0 / 9.0, 2)
    return round(float(temp), 2)


def clean_pm25_series(readings, hourly_medians=None):
    """
    Clean a sequence of (hour, pm25_or_none) readings:
    - Drop/cap out-of-range values (< 0 or > 1000)
    - Forward-fill (LOCF) missing values for gaps <= 2 hours
    - Impute longer gaps using hourly median (if provided) or fallback to last known valid value
    """
    hourly_medians = hourly_medians or {}
    valid = []
    for hour, val in readings:
        if val is None or val < 0 or val > 1000:
            valid.append(None)
        else:
            valid.append(float(val))

    cleaned = list(valid)
    n = len(cleaned)
    i = 0
    while i < n:
        if cleaned[i] is None:
            j = i
            while j < n and cleaned[j] is None:
                j += 1
            gap_len = j - i
            prev_val = cleaned[i - 1] if i > 0 else None
            hour_val = readings[i][0]

            if gap_len <= 2 and prev_val is not None:
                fill_val = prev_val
            elif hour_val in hourly_medians:
                fill_val = hourly_medians[hour_val]
            else:
                fill_val = prev_val if prev_val is not None else 0.0

            for k in range(i, j):
                cleaned[k] = round(fill_val, 2)
            i = j
        else:
            cleaned[i] = round(cleaned[i], 2)
            i += 1

    return [(readings[idx][0], cleaned[idx]) for idx in range(n)]


def deduplicate_records(records):
    """Deduplicate by (station_name, date, hour), keeping the first entry."""
    seen = set()
    unique = []
    for rec in records:
        station = rec["station_name"].strip().title()
        date = rec["date"].strip()
        hour = int(rec["hour"])
        key = (station, date, hour)
        if key not in seen:
            seen.add(key)
            unique.append({**rec, "station_name": station, "date": date, "hour": hour})
    return unique


def min_max_normalise(values):
    """Scale values to [0, 1], rounded to 3 decimal places."""
    if not values:
        return []
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0 for _ in values]
    return [round((v - lo) / (hi - lo), 3) for v in values]


def z_score_standardise(values):
    """Standardise values to mean ~0 and std ~1, rounded to 3 decimal places."""
    if not values:
        return []
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std = variance ** 0.5
    if std == 0:
        return [0.0 for _ in values]
    return [round((v - mean) / std, 3) for v in values]


if __name__ == "__main__":
    sample_series = [(8, 45.0), (9, None), (10, None), (11, -5.0), (12, 72.0)]
    print("Cleaned PM2.5:", clean_pm25_series(sample_series, hourly_medians={11: 60.0}))
    print("Temp 84.2 F -> C:", clean_temperature_c(84.2))
    pm_vals = [45.0, 60.0, 90.0, 120.0]
    print("Min-Max:", min_max_normalise(pm_vals))
    print("Z-Score:", z_score_standardise(pm_vals))
