"""
Module 2: View Current Weather
--------------------------------
Use Case ID: 2
Actors: User, Weather Data Provider, Reporter
Description: Allows users to view the current weather conditions
(temperature, humidity, wind speed, rainfall) of a selected location.

Run standalone: python module2_view_current_weather.py
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests

from weather_api import search_locations, get_current_weather, describe_code


class CurrentWeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("View Current Weather")
        self.geometry("400x420")
        self.configure(bg="#eaf2f8")

        tk.Label(self, text="City Name", bg="#eaf2f8",
                 font=("Segoe UI", 11, "bold")).pack(pady=(15, 5))

        self.city_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.city_var, font=("Segoe UI", 11), width=25)
        entry.pack(pady=5)
        entry.bind("<Return>", lambda e: self.show_weather())
        entry.focus()

        tk.Button(self, text="Get Current Weather", command=self.show_weather,
                  bg="#2e86c1", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=8)

        self.card = tk.Frame(self, bg="white", bd=1, relief="solid")
        self.card.pack(fill="x", padx=20, pady=15)

        self.location_label = tk.Label(self.card, text="--", bg="white",
                                        font=("Segoe UI", 13, "bold"))
        self.location_label.pack(pady=(10, 0))

        self.icon_label = tk.Label(self.card, text="", bg="white", font=("Segoe UI", 32))
        self.icon_label.pack()

        self.temp_label = tk.Label(self.card, text="Temperature: --", bg="white", font=("Segoe UI", 11))
        self.temp_label.pack(pady=2)

        self.humidity_label = tk.Label(self.card, text="Humidity: --", bg="white", font=("Segoe UI", 11))
        self.humidity_label.pack(pady=2)

        self.wind_label = tk.Label(self.card, text="Wind Speed: --", bg="white", font=("Segoe UI", 11))
        self.wind_label.pack(pady=2)

        self.rain_label = tk.Label(self.card, text="Rainfall: --", bg="white", font=("Segoe UI", 11))
        self.rain_label.pack(pady=2)

        self.updated_label = tk.Label(self.card, text="", bg="white", fg="#666", font=("Segoe UI", 8))
        self.updated_label.pack(pady=(2, 10))

        self.status_var = tk.StringVar(value="Enter a city and press Get Current Weather.")
        tk.Label(self, textvariable=self.status_var, bg="#eaf2f8", fg="#333",
                 wraplength=360, font=("Segoe UI", 9)).pack(pady=5)

    def show_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input required", "Please enter a city name.")
            return

        self.status_var.set("Locating city...")
        self.update_idletasks()

        try:
            results = search_locations(city, count=1)
        except requests.RequestException:
            self.status_var.set("Network connection unavailable.")
            return

        if not results:
            self.status_var.set(f"Invalid location entered: '{city}' not found.")
            return

        loc = results[0]
        self.location_label.config(text=f"{loc['name']}, {loc.get('country', '')}")
        self.status_var.set("Fetching current weather data...")
        self.update_idletasks()

        try:
            current = get_current_weather(loc["latitude"], loc["longitude"])
        except requests.RequestException:
            self.status_var.set("Weather data unavailable. API failure or server timeout.")
            return

        desc, icon = describe_code(current.get("weather_code"))
        self.icon_label.config(text=f"{icon}  {desc}")
        self.temp_label.config(text=f"Temperature: {current.get('temperature_2m', '--')} °C")
        self.humidity_label.config(text=f"Humidity: {current.get('relative_humidity_2m', '--')} %")
        self.wind_label.config(text=f"Wind Speed: {current.get('wind_speed_10m', '--')} km/h")
        self.rain_label.config(text=f"Rainfall: {current.get('precipitation', '--')} mm")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_label.config(text=f"Last updated: {now}")
        self.status_var.set("Current weather displayed successfully.")


if __name__ == "__main__":
    app = CurrentWeatherApp()
    app.mainloop()