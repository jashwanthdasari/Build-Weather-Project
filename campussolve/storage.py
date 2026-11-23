"""Local JSON/CSV storage with resilient file initialization."""
import csv, json, os
from datetime import datetime, timezone


class Storage:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.json_path = os.path.join(data_dir, "weather_records.json")
        self.csv_path = os.path.join(data_dir, "weather_records.csv")
        self._initialize()

    def _initialize(self):
        if not os.path.exists(self.json_path):
            self._write_json([])
        if not os.path.exists(self.csv_path):
            self._write_csv([])

    def _write_json(self, records):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

    def _write_csv(self, records):
        fields = self.fields()
        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(records)

    @staticmethod
    def fields():
        return ["city", "country", "latitude", "longitude", "observed_at", "temperature_c", "feels_like_c",
                "humidity_percent", "wind_kmh", "precipitation_mm", "weather_code", "condition", "source"]

    def load(self):
        try:
            with open(self.json_path, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Expected JSON list")
            return data
        except (OSError, json.JSONDecodeError, ValueError):
            # Recover gracefully; preserve the corrupt file for diagnosis.
            if os.path.exists(self.json_path):
                try:
                    os.replace(self.json_path, self.json_path + ".corrupt-" + datetime.now().strftime("%Y%m%d%H%M%S"))
                except OSError:
                    pass
            self._write_json([])
            return []

    def save_record(self, record):
        records = self.load()
        record = dict(record)
        record.setdefault("saved_at", datetime.now(timezone.utc).isoformat())
        records.append(record)
        self._write_json(records)
        self._write_csv(records)
        return record

    def replace_all(self, records):
        self._write_json(records)
        self._write_csv(records)

    def export_csv(self, path, records=None):
        records = self.load() if records is None else records
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields(), extrasaction="ignore")
            writer.writeheader()
            writer.writerows(records)
        return path
