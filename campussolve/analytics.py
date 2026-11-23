"""Weather record filtering and aggregate analytics."""
from statistics import mean
from collections import Counter


def filter_records(records, keyword="", condition="All"):
    keyword = (keyword or "").strip().lower()
    output = []
    for r in records:
        if condition not in ("All", "") and condition.lower() not in str(r.get("condition", "")).lower():
            continue
        haystack = " ".join(str(r.get(k, "")) for k in ("city", "country", "condition", "observed_at", "source")).lower()
        if keyword and keyword not in haystack:
            continue
        output.append(r)
    return output


def summarize(records):
    if not records:
        return {"count": 0, "average_temperature_c": None, "average_humidity_percent": None,
                "average_wind_kmh": None, "min_temperature_c": None, "max_temperature_c": None,
                "conditions": {}, "cities": 0}
    temps = [float(r["temperature_c"]) for r in records if r.get("temperature_c") is not None]
    humidity = [float(r["humidity_percent"]) for r in records if r.get("humidity_percent") is not None]
    wind = [float(r["wind_kmh"]) for r in records if r.get("wind_kmh") is not None]
    return {"count": len(records), "average_temperature_c": round(mean(temps), 1) if temps else None,
            "average_humidity_percent": round(mean(humidity), 1) if humidity else None,
            "average_wind_kmh": round(mean(wind), 1) if wind else None,
            "min_temperature_c": min(temps) if temps else None, "max_temperature_c": max(temps) if temps else None,
            "conditions": dict(Counter(r.get("condition", "Unknown") for r in records)),
            "cities": len(set(r.get("city", "") for r in records))}


def warning_flags(record, hot_c=38, cold_c=0, wind_kmh=50, humidity_percent=90):
    warnings = []
    t, w, h = record.get("temperature_c"), record.get("wind_kmh"), record.get("humidity_percent")
    if t is not None and float(t) >= hot_c: warnings.append(f"High temperature alert (≥{hot_c}°C)")
    if t is not None and float(t) <= cold_c: warnings.append(f"Low temperature alert (≤{cold_c}°C)")
    if w is not None and float(w) >= wind_kmh: warnings.append(f"High wind alert (≥{wind_kmh} km/h)")
    if h is not None and float(h) >= humidity_percent: warnings.append(f"High humidity alert (≥{humidity_percent}%)")
    return warnings
