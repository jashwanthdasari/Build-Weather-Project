"""Open-Meteo geocoding and current-weather API client (no API key required)."""
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json

from .validation import validate_city, validate_coordinates

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
    55: "Dense drizzle", 56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Light rain", 63: "Moderate rain", 65: "Heavy rain", 66: "Light freezing rain",
    67: "Heavy freezing rain", 71: "Light snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains", 80: "Light rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Light snow showers", 86: "Heavy snow showers", 95: "Thunderstorm", 96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail"
}

class WeatherAPIError(RuntimeError):
    pass


def _get_json(url, timeout=10):
    req = Request(url, headers={"User-Agent": "CampusSolveWeatherViewer/1.0"})
    try:
        with urlopen(req, timeout=timeout) as response:
            if response.status != 200:
                raise WeatherAPIError(f"API returned HTTP {response.status}")
            return json.loads(response.read().decode("utf-8"))
    except (URLError, HTTPError, TimeoutError, OSError) as exc:
        raise WeatherAPIError(f"Network request failed: {exc}") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise WeatherAPIError("Weather service returned invalid JSON.") from exc


def geocode_city(city):
    city = validate_city(city)
    params = urlencode({"name": city, "count": 1, "language": "en", "format": "json"})
    payload = _get_json("https://geocoding-api.open-meteo.com/v1/search?" + params)
    results = payload.get("results") or []
    if not results:
        raise WeatherAPIError(f"No location found for '{city}'. Try another spelling.")
    place = results[0]
    return {"name": place.get("name", city), "country": place.get("country", ""),
            "latitude": float(place["latitude"]), "longitude": float(place["longitude"]),
            "timezone": place.get("timezone", "UTC")}


def fetch_current_weather(latitude, longitude, location=None):
    latitude, longitude = validate_coordinates(latitude, longitude)
    params = urlencode({"latitude": latitude, "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
        "timezone": "auto"})
    payload = _get_json("https://api.open-meteo.com/v1/forecast?" + params)
    current = payload.get("current")
    if not current:
        raise WeatherAPIError("Weather API returned no current-weather data.")
    return {
        "city": (location or {}).get("name", "Unknown"),
        "country": (location or {}).get("country", ""),
        "latitude": latitude, "longitude": longitude,
        "observed_at": current.get("time", datetime.now(timezone.utc).isoformat()),
        "temperature_c": current.get("temperature_2m"),
        "feels_like_c": current.get("apparent_temperature"),
        "humidity_percent": current.get("relative_humidity_2m"),
        "wind_kmh": current.get("wind_speed_10m"),
        "precipitation_mm": current.get("precipitation"),
        "weather_code": current.get("weather_code"),
        "condition": WEATHER_CODES.get(current.get("weather_code"), "Unknown condition"),
        "source": "Open-Meteo"
    }


def lookup_weather(city):
    place = geocode_city(city)
    return fetch_current_weather(place["latitude"], place["longitude"], place)
