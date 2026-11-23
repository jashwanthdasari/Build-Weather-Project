"""Small optional Tkinter desktop interface."""
import tkinter as tk
from tkinter import ttk, messagebox
from .weather_api import lookup_weather, WeatherAPIError
from .storage import Storage
from .analytics import summarize

class WeatherGUI:
    def __init__(self, storage):
        self.storage = storage
        self.root = tk.Tk()
        self.root.title("CampusSolve • Public API Weather Viewer")
        self.root.geometry("780x540")
        self.root.minsize(620, 400)
        style = ttk.Style(self.root)
        try: style.theme_use("clam")
        except tk.TclError: pass
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="CampusSolve Weather Viewer", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Fetch live weather • Save local records • Review summary", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 12))
        top = ttk.Frame(frame); top.pack(fill="x")
        self.city = tk.StringVar()
        ttk.Label(top, text="City:").pack(side="left")
        entry = ttk.Entry(top, textvariable=self.city, width=32); entry.pack(side="left", padx=6); entry.bind("<Return>", lambda _e: self.fetch())
        ttk.Button(top, text="Fetch & Save", command=self.fetch).pack(side="left", padx=4)
        ttk.Button(top, text="Summary", command=self.show_summary).pack(side="left", padx=4)
        self.output = tk.Text(frame, height=20, wrap="word", font=("Consolas", 10))
        self.output.pack(fill="both", expand=True, pady=12)
        self.output.insert("end", "Welcome! Enter a city above to fetch current conditions.\n")
        self.root.mainloop()
    def fetch(self):
        city = self.city.get().strip()
        if not city:
            messagebox.showwarning("Validation", "Please enter a city name."); return
        self.output.insert("end", f"Fetching weather for {city}...\n"); self.root.update_idletasks()
        try:
            record = lookup_weather(city)
            self.storage.save_record(record)
            self.output.insert("end", f"Saved: {record['city']}, {record['country']}\nTemperature: {record['temperature_c']} °C\nFeels like: {record['feels_like_c']} °C\nHumidity: {record['humidity_percent']}%\nWind: {record['wind_kmh']} km/h\nCondition: {record['condition']}\n\n")
        except (WeatherAPIError, OSError, ValueError) as exc:
            messagebox.showerror("Weather lookup failed", str(exc))
    def show_summary(self):
        s = summarize(self.storage.load())
        self.output.insert("end", f"\nSummary: {s['count']} records, {s['cities']} unique cities\nAvg temperature: {s['average_temperature_c']} °C | Avg humidity: {s['average_humidity_percent']}% | Avg wind: {s['average_wind_kmh']} km/h\n\n")

def launch_gui(storage):
    WeatherGUI(storage)
