"""Report exports: Markdown, text, CSV."""
from datetime import datetime
from .analytics import summarize


def build_report(records):
    stats = summarize(records)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = ["# CampusSolve Weather Viewer Report", f"Generated: {now}", "", "## Executive Summary",
        f"- Records: {stats['count']}", f"- Cities represented: {stats['cities']}",
        f"- Average temperature: {stats['average_temperature_c'] if stats['average_temperature_c'] is not None else 'N/A'} °C",
        f"- Average humidity: {stats['average_humidity_percent'] if stats['average_humidity_percent'] is not None else 'N/A'} %",
        f"- Average wind: {stats['average_wind_kmh'] if stats['average_wind_kmh'] is not None else 'N/A'} km/h",
        f"- Temperature range: {stats['min_temperature_c'] if stats['min_temperature_c'] is not None else 'N/A'} to {stats['max_temperature_c'] if stats['max_temperature_c'] is not None else 'N/A'} °C", "", "## Conditions"]
    for condition, count in sorted(stats["conditions"].items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"- {condition}: {count}")
    lines += ["", "## Records", "| City | Country | Temp °C | Feels °C | Humidity % | Wind km/h | Rain mm | Condition | Observed |",
        "|---|---|---:|---:|---:|---:|---:|---|---|"]
    for r in records:
        lines.append("| " + " | ".join(str(r.get(k, "")) for k in ["city", "country", "temperature_c", "feels_like_c", "humidity_percent", "wind_kmh", "precipitation_mm", "condition", "observed_at"]) + " |")
    return "\n".join(lines) + "\n"


def export_report(records, directory="exports"):
    import os
    os.makedirs(directory, exist_ok=True)
    report = build_report(records)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outputs = []
    for ext in ("md", "txt"):
        path = os.path.join(directory, f"weather_report_{stamp}.{ext}")
        with open(path, "w", encoding="utf-8") as f: f.write(report)
        outputs.append(path)
    return outputs
