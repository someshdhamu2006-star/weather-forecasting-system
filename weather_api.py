"""
weather_api.py
--------------
Shared helper functions for calling the Open-Meteo API.
Used by all four use-case modules:
  1. search_location.py
  2. view_current_weather.py
  3. view_weather_forecast.py
  4. refresh_weather_data.py

No API key required.
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: ("Clear sky", "☀️"), 1: ("Mainly clear", "🌤️"), 2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"), 45: ("Fog", "🌫️"), 48: ("Rime fog", "🌫️"),
    51: ("Light drizzle", "🌦️"), 53: ("Moderate drizzle", "🌦️"), 55: ("Dense drizzle", "🌧️"),
    61: ("Slight rain", "🌦️"), 63: ("Moderate rain", "🌧️"), 65: ("Heavy rain", "🌧️"),
    71: ("Slight snow", "🌨️"), 73: ("Moderate snow", "🌨️"), 75: ("Heavy snow", "❄️"),
    80: ("Rain showers", "🌦️"), 81: ("Moderate showers", "🌧️"), 82: ("Violent showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"), 96: ("Thunderstorm w/ hail", "⛈️"), 99: ("Severe thunderstorm", "⛈️"),
}


def describe_code(code):
    """Translate a WMO weather code into (description, icon)."""
    return WEATHER_CODES.get(code, ("Unknown", "❔"))


def search_locations(query, count=5):
    """
    Use Case 1 support: search for locations matching a name.
    Returns a list of dicts: name, country, admin1, latitude, longitude.
    Raises requests.RequestException on network failure.
    """
    resp = requests.get(GEOCODE_URL, params={"name": query, "count": count}, timeout=10)
    resp.raise_for_status()
    return resp.json().get("results", [])


def get_current_weather(lat, lon):
    """
    Use Case 2 support: get current weather for a coordinate.
    Returns a dict with temperature_2m, relative_humidity_2m, wind_speed_10m,
    precipitation, weather_code.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,weather_code",
        "timezone": "auto",
    }
    resp = requests.get(FORECAST_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json().get("current", {})


def get_forecast(lat, lon, days=7):
    """
    Use Case 3 support: get multi-day forecast for a coordinate.
    Returns a dict with lists: time, weather_code, temperature_2m_max,
    temperature_2m_min, precipitation_sum.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "forecast_days": days,
        "timezone": "auto",
    }
    resp = requests.get(FORECAST_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json().get("daily", {})
