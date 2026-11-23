# CampusSolve — Public API Weather Viewer (Project #111)

A beginner-friendly Python weather application that retrieves live current weather from **Open-Meteo** (no API key required), validates inputs, saves records locally, supports searching and analytics, and exports reports/charts.

## Features
- Menu-driven terminal application with guided actions
- Live city geocoding and current weather retrieval (Open-Meteo)
- Defensive validation of city and coordinate inputs; safe handling of network/API failures
- Persistent local weather history in JSON and CSV
- Keyword and condition filtering
- Executive analytics (record/city totals, averages, min/max, condition distribution)
- Configurable threshold warning indicators (temperature, wind, humidity)
- Report export to Markdown and plain text, plus CSV records
- Bulk CSV import with row validation and import-error log
- Matplotlib temperature trend and histogram chart exports
- Optional Tkinter GUI (available on Python installations that include Tk)
- Included 36-record realistic demonstration dataset with edge and boundary cases
- Automated tests for validation, analytics, storage, import/export, API parsing and plots

## Requirements
- Python 3.10 or later
- Internet access for live weather lookups
- Matplotlib for chart features (`pip install -r requirements.txt`); GUI is optional and uses Tkinter from Python

The main application otherwise uses Python's standard library.

## Run
1. Extract the ZIP.
2. Open a terminal in the project folder.
3. Install chart dependency: `python -m pip install -r requirements.txt`
4. Start: `python main.py` (Windows: double-click `run_windows.bat`)

On Linux/macOS, `./run_unix.sh` is also available.

## Demo walkthrough
1. Choose **1** and enter a city (e.g., Hyderabad) to fetch/save weather.
2. Try an invalid city or blank input to demonstrate defensive handling.
3. Choose **2** to filter records using a keyword and/or condition.
4. Choose **3** for executive summary and trend metrics.
5. Choose **4** to generate Markdown, TXT, and CSV reports under `exports/`.
6. Choose **5** to import a CSV dataset; invalid rows are reported in `exports/import_errors.log`.
7. Choose **6** or **7** to show temperature trend or distribution charts in `charts/`.
8. Choose **8** to launch the optional GUI.

## Data files
- `data/weather_records.json` — canonical saved history (initialized automatically)
- `data/weather_records.csv` — synchronized tabular copy
- `data/sample_weather_records.csv` — seed/demo data (36 records)
- `exports/` — generated report files and import error logs
- `charts/` — generated charts

The app creates initial storage files when absent. If JSON storage is malformed, it safely resets the dataset and attempts to preserve the damaged file with a timestamped `.corrupt-*` name.


## Import CSV format
Required headers: `city`, `temperature_c`, `humidity_percent`, `wind_kmh`. Optional headers include `country`, `latitude`, `longitude`, `observed_at`, `feels_like_c`, `precipitation_mm`, `weather_code`, `condition`, `source`.

## Tests
Run: `python -m unittest discover -s tests -v`

Tests are offline and mock the API layer. They do not require API access. A live API test can be performed through the interactive menu if internet access is available.

## API reference
- Geocoding: https://geocoding-api.open-meteo.com/v1/search
- Current weather: https://api.open-meteo.com/v1/forecast
- Provider: Open-Meteo (attribution to provider is included in saved records)

## Thresholds
Default warnings: hot >= 38°C, cold <= 0°C, wind >= 50 km/h, humidity >= 90%. Threshold checks are simple demo safety indicators, not official alerts.

## Project brief alignment
Implements the mandatory CLI, validation, API logic, JSON/CSV persistence, search, executive summary, Matplotlib plotting; and stretch report exports, threshold warnings, optional GUI, and CSV bulk import.
