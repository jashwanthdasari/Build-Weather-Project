# Project Report — CampusSolve Public API Weather Viewer

## 1. Overview
Public API Weather Viewer is a Python application for fetching live weather conditions from Open-Meteo and maintaining a local, searchable record history. It targets students and demonstrators who need an approachable public API workflow without API-key registration.

## 2. Objectives
- Retrieve live current-weather values from a public API
- Sanitize and validate user inputs and API responses
- Persist structured data locally in JSON and CSV
- Search and filter saved observations
- Produce useful aggregate statistics and trend visuals
- Export reports for presentation/review

## 3. Architecture
The project uses modular Python components:
- `cli.py` — terminal menu, prompts and user journey orchestration
- `weather_api.py` — geocoding, HTTP calls, API normalization, WMO condition labels
- `validation.py` — city, numeric, and coordinate validation
- `storage.py` — resilient JSON persistence and CSV synchronization
- `analytics.py` — filters, aggregates, and alert thresholds
- `importer.py` — bulk CSV import with per-row error capture
- `reports.py` — Markdown/TXT report builder and exports
- `plotting.py` — Matplotlib trend and distribution charts
- `gui.py` — optional Tkinter front end


## 4. Feature Demonstration
The app has a menu for live fetch, record browsing, analytics, multi-format export, CSV import, chart generation, optional GUI, and exit. Seed data provides 36 example records for offline demo.


## 5. Data Fields
Records include city/country, coordinates, observation time, temperature, apparent temperature, humidity, wind speed, precipitation, weather code, readable condition, and source/provider metadata.


## 6. Validation and Fault Tolerance
- Blank/invalid city names are rejected before geocoding
- Numeric fields are parsed and range-checked
- Latitude/longitude bounds are checked
- Network errors/timeouts and invalid service responses are converted into friendly API errors
- JSON read errors and corrupt files recover with a clean data store while preserving the damaged file where possible
- CSV imports require core headers and validate each row; errors are logged by line


## 7. Analytics
The summary reports record count, unique city count, mean temperature/humidity/wind, min/max temperatures, and condition counts. Alert thresholds flag hot/cold temperatures, high winds, and high humidity.


## 8. Export and Visualization
Reports export Markdown and plain text with a tabular dataset summary; CSV is available for record exchange. Charts include a record-order temperature line plot and a temperature histogram.


## 9. Testing
Automated offline tests cover city and numeric validation, coordinate bounds, persistence, corrupt JSON recovery, filters, aggregate statistics, alert thresholds, CSV imports (valid and invalid), report export, API response parsing using mocks, and chart file generation. Tests are run with `python -m unittest discover -s tests -v`.


## 10. Limitations
- Live weather lookups require network access
- The bundled sample data is synthetic and is labeled `Sample Dataset`; it should not be interpreted as live conditions
- The optional Tkinter GUI depends on a Python distribution with Tk installed and a graphical display
- Alert thresholds are demonstration indicators, not official weather warnings


## 11. Conclusion
This project provides a modular, testable Python application demonstrating public API access, validation, persistence, search, reporting, plotting, optional graphical UI, and bulk import. Its offline demo dataset and automated tests make the core workflows repeatable during a project evaluation.
