"""
Module 3: View Weather Forecast
----------------------------------
Use Case ID: 3
Actors: User, Weather Data Analyzer, Weather Data Provider
Description: Enables users to view future weather predictions (next 5-7 days)
for a selected location, using graphs/tables for readability.

Run standalone: python module3_view_weather_forecast.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests

from weather_api import search_locations, get_forecast, describe_code


class ForecastApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("View Weather Forecast")
        self.geometry("520x420")
        self.configure(bg="#eaf2f8")

        tk.Label(self, text="City Name", bg="#eaf2f8",
                 font=("Segoe UI", 11, "bold")).pack(pady=(15, 5))

        self.city_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.city_var, font=("Segoe UI", 11), width=25)
        entry.pack(pady=5)
        entry.bind("<Return>", lambda e: self.show_forecast())
        entry.focus()

        tk.Button(self, text="Get 7-Day Forecast", command=self.show_forecast,
                  bg="#2e86c1", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=8)

        self.location_label = tk.Label(self, text="", bg="#eaf2f8", font=("Segoe UI", 11, "bold"))
        self.location_label.pack()

        columns = ("date", "condition", "max", "min", "rain")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=7)
        self.tree.heading("date", text="Date")
        self.tree.heading("condition", text="Condition")
        self.tree.heading("max", text="Max °C")
        self.tree.heading("min", text="Min °C")
        self.tree.heading("rain", text="Rain (mm)")
        self.tree.column("date", width=100)
        self.tree.column("condition", width=170)
        self.tree.column("max", width=70, anchor="center")
        self.tree.column("min", width=70, anchor="center")
        self.tree.column("rain", width=80, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        self.status_var = tk.StringVar(value="Enter a city and press Get 7-Day Forecast.")
        tk.Label(self, textvariable=self.status_var, bg="#eaf2f8", fg="#333",
                 wraplength=480, font=("Segoe UI", 9)).pack(pady=5)

    def show_forecast(self):
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
        self.location_label.config(text=f"Forecast for {loc['name']}, {loc.get('country', '')}")
        self.status_var.set("Processing forecast data...")
        self.update_idletasks()

        try:
            daily = get_forecast(loc["latitude"], loc["longitude"], days=7)
        except requests.RequestException:
            self.status_var.set("Forecast data unavailable. Processing error or API failure.")
            return

        self.tree.delete(*self.tree.get_children())
        dates = daily.get("time", [])
        codes = daily.get("weather_code", [])
        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])
        rain = daily.get("precipitation_sum", [])

        for i, date_str in enumerate(dates):
            desc, icon = describe_code(codes[i]) if i < len(codes) else ("--", "")
            self.tree.insert("", "end", values=(
                date_str,
                f"{icon} {desc}",
                tmax[i] if i < len(tmax) else "--",
                tmin[i] if i < len(tmin) else "--",
                rain[i] if i < len(rain) else "--",
            ))

        self.status_var.set(f"Forecast displayed for the next {len(dates)} days.")


if __name__ == "__main__":
    app = ForecastApp()
    app.mainloop()