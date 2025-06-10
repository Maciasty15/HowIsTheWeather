import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Inicjalizacja zmiennych środowiskowych
load_dotenv()

# Stałe API
OPENMETO_BASE_URL = os.getenv("WEATHERAPI_API_BASE_URL") 

def get_coordinates(location) -> (tuple[str, str] | tuple[None, None]):
    url = f"{OPENMETO_BASE_URL}search?name={location}&count=1&language=pl&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            result = data["results"][0]
            return result["latitude"], result["longitude"]
    return None, None


def get_weather(location) -> str:
    lat, lon = get_coordinates(location)
    if lat is None or lon is None:
        return "Nie udało się znaleźć współrzędnych dla podanej lokalizacji."

    url = (
        f"{OPENMETO_BASE_URL}forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "current_weather" in data:
            weather = data["current_weather"]
            temperature = weather["temperature"]
            windspeed = weather["windspeed"]
            weather_code = weather["weathercode"]

            # Prosty mapping kodu pogodowego na opis (pełna lista: https://open-meteo.com/en/docs#weathercode)
            weather_description = {
                0: "Bezchmurnie",
                1: "Głównie bezchmurnie",
                2: "Częściowe zachmurzenie",
                3: "Zachmurzenie duże",
                45: "Mgła",
                48: "Osadzająca się mgła",
                51: "Lekka mżawka",
                53: "Umiarkowana mżawka",
                55: "Gęsta mżawka",
                61: "Lekki deszcz",
                63: "Umiarkowany deszcz",
                65: "Silny deszcz",
                71: "Lekki śnieg",
                73: "Umiarkowany śnieg",
                75: "Gęsty śnieg",
                95: "Burza",
            }.get(weather_code, "Nieznana pogoda")

            return f"{weather_description}, temperatura: {temperature}°C, wiatr: {windspeed} km/h"
        else:
            return "Nie udało się pobrać danych pogodowych."
    else:
        return "Błąd przy pobieraniu danych pogodowych."
