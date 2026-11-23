"""Menu-driven terminal application."""
import os, sys
from .storage import Storage
from .weather_api import lookup_weather, WeatherAPIError
from .analytics import summarize, filter_records, warning_flags
from .reports import export_report
from .importer import import_csv

BANNER = """╔════════════════════════════════════════════════════════════╗
║       CampusSolve | PUBLIC API WEATHER VIEWER               ║
║       Weather insights • local records • reports          ║
╚════════════════════════════════════════════════════════════╝"""

def fmt(value, unit=""):
    return "N/A" if value is None else f"{value}{unit}"

def show_record(r):
    print(f"\n  {r.get('city')}, {r.get('country','')}")
    print(f"  Condition: {r.get('condition')} | Temperature: {fmt(r.get('temperature_c'),' °C')} | Feels like: {fmt(r.get('feels_like_c'),' °C')}")
    print(f"  Humidity: {fmt(r.get('humidity_percent'),' %')} | Wind: {fmt(r.get('wind_kmh'),' km/h')} | Rain: {fmt(r.get('precipitation_mm'),' mm')}")
    print(f"  Observed: {r.get('observed_at')} | Source: {r.get('source','')}")
    alerts = warning_flags(r)
    if alerts:
        print("  ⚠ ALERTS: " + " | ".join(alerts))

def pause():
    input("\nPress Enter to return to menu...")

def run():
    os.makedirs("data", exist_ok=True); os.makedirs("exports", exist_ok=True); os.makedirs("charts", exist_ok=True)
    store = Storage("data")
    while True:
        print(BANNER)
        print(" [1] Fetch live weather & save record")
        print(" [2] Browse / search saved records")
        print(" [3] Executive summary")
        print(" [4] Export reports (Markdown + TXT + CSV)")
        print(" [5] Import records from CSV")
        print(" [6] Plot temperature trend")
        print(" [7] Plot temperature distribution")
        print(" [8] Launch optional GUI")
        print(" [9] Exit")
        choice = input("\nSelect an option [1-9]: ").strip()
        if choice == "1":
            city = input("City name: ").strip()
            try:
                record = lookup_weather(city)
                store.save_record(record)
                print("\n✓ Weather fetched and saved successfully.")
                show_record(record)
            except (WeatherAPIError, ValueError, OSError, TimeoutError) as exc:
                print(f"\n✗ Could not fetch weather: {exc}")
            pause()
        elif choice == "2":
            records = store.load()
            keyword = input("Keyword (city/country/condition; Enter for all): ").strip()
            print("Condition options: All, Clear sky, Mainly clear, Partly cloudy, Overcast, Rain, Snow, Thunderstorm, Fog")
            condition = input("Exact condition filter (or All): ").strip() or "All"
            matches = filter_records(records, keyword, condition)
            print(f"\nFound {len(matches)} matching record(s).")
            if not matches: print("No records match your search.")
            for i, r in enumerate(matches[-25:], 1):
                print(f"{i:>2}. {r.get('city')} ({r.get('country','')}) | {r.get('temperature_c')} °C | {r.get('condition')} | {r.get('observed_at')}")
            if len(matches) > 25: print("Showing latest 25 results for readability.")
            pause()
        elif choice == "3":
            s = summarize(store.load())
            print("\n════════ EXECUTIVE SUMMARY ════════")
            print(f"Records: {s['count']} | Unique cities: {s['cities']}")
            print(f"Average temperature: {fmt(s['average_temperature_c'], ' °C')} | Range: {fmt(s['min_temperature_c'], ' °C')} to {fmt(s['max_temperature_c'], ' °C')}")
            print(f"Average humidity: {fmt(s['average_humidity_percent'],' %')} | Average wind: {fmt(s['average_wind_kmh'],' km/h')}")
            print("Condition totals:")
            for cond, count in sorted(s['conditions'].items(), key=lambda item: (-item[1], item[0])): print(f"  • {cond}: {count}")
            pause()
        elif choice == "4":
            records = store.load()
            if not records: print("No records to export yet.")
            else:
                try:
                    files = export_report(records, "exports")
                    csv_path = os.path.join("exports", "weather_records_export.csv")
                    store.export_csv(csv_path, records); files.append(csv_path)
                    print("Exported reports:"); [print("  ✓ " + path) for path in files]
                except OSError as exc: print("Export failed:", exc)
            pause()
        elif choice == "5":
            path = input("CSV file path to import: ").strip().strip('"')
            imported, errors = import_csv(path)
            if imported:
                existing = store.load(); existing.extend(imported); store.replace_all(existing)
                print(f"✓ Imported {len(imported)} record(s).")
            else: print("No records imported.")
            if errors:
                log_path = os.path.join("exports", "import_errors.log")
                with open(log_path, "w", encoding="utf-8") as f: f.write("\n".join(errors) + "\n")
                print(f"{len(errors)} issue(s) logged to {log_path}:")
                for err in errors[:8]: print("  - " + err)
            pause()
        elif choice in ("6", "7"):
            records = store.load()
            if not records: print("No records to plot. Fetch weather or import data first.")
            else:
                try:
                    from .plotting import plot_temperature, plot_distribution
                    if choice == "6":
                        path = "charts/temperature_trend.png"; plot_temperature(records, path, show=True)
                    else:
                        path = "charts/temperature_distribution.png"; plot_distribution(records, path, show=True)
                    print(f"Chart saved to {path}")
                except (RuntimeError, ValueError, OSError) as exc: print("Chart unavailable:", exc)
            pause()
        elif choice == "8":
            try:
                from .gui import launch_gui
                launch_gui(store)
            except Exception as exc: print("GUI could not start (Tkinter may not be installed):", exc)
            pause()
        elif choice == "9":
            print("Thank you for using CampusSolve Weather Viewer. Stay weather-aware! ☁")
            return
        else:
            print("Invalid menu option. Please enter a number from 1 to 9.")
            pause()

if __name__ == "__main__":
    run()
