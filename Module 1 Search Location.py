"""
Module 1: Search Location
--------------------------
Use Case ID: 1
Actors: User, Reporter, Administrator
Description: Allows the user to search for a specific location to obtain
weather information. Supports selecting from suggested results, and
handles invalid location / network errors.

Run standalone: python module1_search_location.py
"""

import tkinter as tk
from tkinter import messagebox
import requests

from weather_api import search_locations


class SearchLocationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Search Location")
        self.geometry("420x360")
        self.configure(bg="#eaf2f8")
        self.selected_location = None  # result of a successful search + selection

        tk.Label(self, text="Enter Location Name", bg="#eaf2f8",
                 font=("Segoe UI", 11, "bold")).pack(pady=(15, 5))

        self.search_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.search_var, font=("Segoe UI", 11), width=28)
        entry.pack(pady=5)
        entry.bind("<Return>", lambda e: self.search())
        entry.focus()

        tk.Button(self, text="Search", command=self.search, bg="#2e86c1",
                  fg="white", font=("Segoe UI", 10, "bold")).pack(pady=5)

        tk.Label(self, text="Suggested Results (select one):", bg="#eaf2f8",
                 font=("Segoe UI", 9)).pack(pady=(10, 0))

        self.results_box = tk.Listbox(self, width=45, height=8, font=("Segoe UI", 9))
        self.results_box.pack(pady=5)
        self.results_box.bind("<<ListboxSelect>>", self.on_select)
        self._results_data = []

        self.status_var = tk.StringVar(value="Enter a city name and press Search.")
        tk.Label(self, textvariable=self.status_var, bg="#eaf2f8",
                 fg="#333", wraplength=380, font=("Segoe UI", 9)).pack(pady=10)

    def search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Input required", "Please enter a location name.")
            return

        self.status_var.set("Searching...")
        self.update_idletasks()

        try:
            results = search_locations(query)
        except requests.RequestException:
            self.status_var.set("Network connection unavailable. Please try again.")
            return

        if not results:
            self.status_var.set(f"Invalid location entered. No results found for '{query}'.")
            self.results_box.delete(0, tk.END)
            return

        self._results_data = results
        self.results_box.delete(0, tk.END)
        for r in results:
            label = f"{r['name']}, {r.get('admin1', '')} {r.get('country', '')}".strip()
            self.results_box.insert(tk.END, label)

        self.status_var.set(f"Found {len(results)} location(s). Select one from the list.")

    def on_select(self, event):
        selection = self.results_box.curselection()
        if not selection:
            return
        result = self._results_data[selection[0]]
        self.selected_location = {
            "name": result["name"],
            "country": result.get("country", ""),
            "lat": result["latitude"],
            "lon": result["longitude"],
        }
        self.status_var.set(
            f"Selected: {self.selected_location['name']}, {self.selected_location['country']} "
            f"(lat={self.selected_location['lat']}, lon={self.selected_location['lon']})"
        )


if __name__ == "__main__":
    app = SearchLocationApp()
    app.mainloop()