import requests
import json
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

API_KEY_FILE = "./api.txt"


def get_api_key_from_file(file_path=API_KEY_FILE):
    try:
        with open(file_path, "r") as f:
            api_key = f.readline().strip()
            if not api_key:
                raise ValueError("API key file is empty or does not contain a key.")
            return api_key
    except FileNotFoundError:
        messagebox.showerror(
            "Ошибка файла", f"Файл '{file_path}' не найден в директории скрипта."
        )
        return None
    except ValueError as e:
        messagebox.showerror("Ошибка ключа", str(e))
        return None


def get_weather():
    city_name = city_entry.get()
    if not city_name:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    api_key = get_api_key_from_file()
    if api_key is None:
        return

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lang": "ru", "units": "metric", "q": city_name, "appid": api_key}

    try:
        response = requests.get(url, params)
        response.raise_for_status()
        weather_data = response.json()

        weather_description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        wind_speed = weather_data["wind"]["speed"]
        humidity = weather_data["main"]["humidity"]

        result_text = (
            f"Weather in {city_name}:\n"
            f"{weather_description}, temperature: {temperature}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Wind: {wind_speed} m/s\n"
            f"Humidity: {humidity}%"
        )
        result_label.config(text=result_text)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Error during API request: {e}")
        result_label.config(text="Error getting data.")
    except json.JSONDecodeError:
        messagebox.showerror("Data Error", "Failed to process data from the server.")
        result_label.config(text="Data processing error.")
    except KeyError:
        messagebox.showerror("Data Error", "Invalid data format from the server.")
        result_label.config(text="Invalid data format.")


root = tk.Tk()
root.title("Weather in City")
root.geometry("400x300")
root.resizable(width=True, height=True)

instruction_label = ttk.Label(root, text="Enter city name:")
instruction_label.pack(padx=10, pady=10)

city_entry = ttk.Entry(root, width=30)
city_entry.pack(padx=10, pady=5)
city_entry.focus_set()

weather_button = ttk.Button(root, text="Get Weather", command=get_weather)
weather_button.pack(padx=10, pady=10)

result_label = ttk.Label(root, text="", justify="left")
result_label.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()
