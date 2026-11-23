"""Bulk CSV importer with row-level validation and an error log."""
import csv
from datetime import datetime, timezone
from .validation import validate_float, validate_city

REQUIRED = ("city", "temperature_c", "humidity_percent", "wind_kmh")

def import_csv(path):
    accepted, errors = [], []
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return [], ["CSV is empty or has no header row."]
            missing = [name for name in REQUIRED if name not in reader.fieldnames]
            if missing:
                return [], ["Missing required columns: " + ", ".join(missing)]
            for line_no, row in enumerate(reader, start=2):
                try:
                    city = validate_city(row.get("city") or "")
                    temp = validate_float(row.get("temperature_c"), "temperature", -100, 70)
                    humidity = validate_float(row.get("humidity_percent"), "humidity", 0, 100)
                    wind = validate_float(row.get("wind_kmh"), "wind", 0, 400)
                    record = {"city": city, "country": row.get("country", ""), "latitude": row.get("latitude", ""),
                        "longitude": row.get("longitude", ""), "observed_at": row.get("observed_at") or datetime.now(timezone.utc).isoformat(),
                        "temperature_c": temp, "feels_like_c": validate_float(row.get("feels_like_c") or temp, "feels-like", -100, 70),
                        "humidity_percent": humidity, "wind_kmh": wind,
                        "precipitation_mm": validate_float(row.get("precipitation_mm") or 0, "precipitation", 0, 1000),
                        "weather_code": row.get("weather_code", ""), "condition": row.get("condition", "Imported"),
                        "source": row.get("source", "CSV Import")}
                    accepted.append(record)
                except (ValueError, TypeError) as exc:
                    errors.append(f"Line {line_no}: {exc}")
    except OSError as exc:
        return [], [f"Unable to read file: {exc}"]
    return accepted, errors
