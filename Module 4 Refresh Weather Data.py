"""
Module 4: Refresh Weather Data
---------------------------------
Use Case ID: 4
Actors: User, Administrator, Weather Data Provider
Description: Allows the system to retrieve and display the latest weather
information, either manually (Refresh button) or automatically at a
predefined interval (simulating "system policy" refresh).

Run standalone: python module4_refresh_weather_data.py
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests

from weather_api import search_locations, get_current_weather, describe_code

AUTO_REFRESH_SECONDS = 60  # simulated "system policy" refresh interval


class RefreshWeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Refresh Weather Data")
        self.geometry("400x400")
        self.configure(bg="#eaf2f8")

        self.selected_location = None
        self.auto_refresh_enabled = tk.BooleanVar(value=False)
        self._after_id = None

        tk.Label(self, text="City Name", bg="#eaf2f8",
                 font=("Segoe UI", 11, "bold")).pack(pady=(15, 5))

        self.city_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.city_var, font=("Segoe UI", 11), width=25)
        entry.pack(pady=5)
        entry.bind("<Return>", lambda e: self.load_location())
        entry.focus()

        tk.Button(self, text="Load Location", command=self.load_location,
                  bg="#2e86c1", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=5)

        tk.Button(self, text="⟳ Refresh Now", command=self.refresh_now,
                  bg="#28b463", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=5)

        tk.Checkbutton(self, text=f"Auto-refresh every {AUTO_REFRESH_SECONDS}s",
                       variable=self.auto_refresh_enabled, bg="#eaf2f8",
                       command=self.toggle_auto_refresh,
                       font=("Segoe UI", 9)).pack(pady=5)

        self.card = tk.Frame(self, bg="white", bd=1, relief="solid")
        self.card.pack(fill="x", padx=20, pady=10)

        self.location_label = tk.Label(self.card, text="--", bg="white", font=("Segoe UI", 12, "bold"))
        self.location_label.pack(pady=(10, 0))

        self.icon_label = tk.Label(self.card, text="", bg="white", font=("Segoe UI", 26))
        self.icon_label.pack()

        self.temp_label = tk.Label(self.card, text="Temperature: --", bg="white", font=("Segoe UI", 10))
        self.temp_label.pack(pady=2)

        self.updated_label = tk.Label(self.card, text="Last updated: --", bg="white",
                                       fg="#666", font=("Segoe UI", 9))
        self.updated_label.pack(pady=(2, 10))

        self.status_var = tk.StringVar(value="Enter a city and press Load Location.")
        tk.Label(self, textvariable=self.status_var, bg="#eaf2f8", fg="#333",
                 wraplength=360, font=("Segoe UI", 9)).pack(pady=5)

    def load_location(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input required", "Please enter a city name.")
            return

        self.status_var.set("Locating city...")
        self.update_idletasks()

        try:
            results = search_locations(city, count=1)
        except requests.RequestException:
            self.status_var.set("Network error while locating city.")
            return

        if not results:
            self.status_var.set(f"Invalid location entered: '{city}' not found.")
            return

        loc = results[0]
        self.selected_location = {
            "name": loc["name"],
            "country": loc.get("country", ""),
            "lat": loc["latitude"],
            "lon": loc["longitude"],
        }
        self.location_label.config(text=f"{loc['name']}, {loc.get('country', '')}")
        self.refresh_now()

    def refresh_now(self):
        """Manually triggered refresh (User clicks Refresh)."""
        if not self.selected_location:
            messagebox.showinfo("No location", "Please load a location first.")
            return

        self.status_var.set("Refreshing weather data...")
        self.update_idletasks()

        try:
            current = get_current_weather(self.selected_location["lat"], self.selected_location["lon"])
        except requests.RequestException:
            self.status_var.set("Server timeout / network error. Refresh failed.")
            return

        desc, icon = describe_code(current.get("weather_code"))
        self.icon_label.config(text=f"{icon}  {desc}")
        self.temp_label.config(text=f"Temperature: {current.get('temperature_2m', '--')} °C")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_label.config(text=f"Last updated: {now}")
        self.status_var.set("Latest weather data displayed successfully.")

    def toggle_auto_refresh(self):
        """Simulates 'System automatically refreshes data at predefined intervals.'"""
        if self.auto_refresh_enabled.get():
            self.status_var.set(f"Auto-refresh enabled (every {AUTO_REFRESH_SECONDS}s).")
            self._schedule_auto_refresh()
        else:
            if self._after_id:
                self.after_cancel(self._after_id)
                self._after_id = None
            self.status_var.set("Auto-refresh disabled.")

    def _schedule_auto_refresh(self):
        if self.auto_refresh_enabled.get():
            self.refresh_now()
            self._after_id = self.after(AUTO_REFRESH_SECONDS * 1000, self._schedule_auto_refresh)


if __name__ == "__main__":
    app = RefreshWeatherApp()
    app.mainloop()