import os
import requests
import urllib.parse
from dotenv import load_dotenv

# Inicjalizacja zmiennych środowiskowych
load_dotenv()

# Stałe API
OPENMETO_BASE_URL = os.getenv(
    "WEATHERAPI_API_BASE_URL", "https://air-quality-api.open-meteo.com/"
)
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/"


def get_coordinates(location) -> tuple[str, str] | tuple[None, None]:
    print(f"Original location name: {location}")

    # Encode the location name properly for URL
    encoded_location = urllib.parse.quote(location)
    print(f"URL-encoded location name: {encoded_location}")

    url = f"{GEOCODING_API_URL}search?name={encoded_location}&count=1&format=json"
    print(f"Searching coordinates for location: {location}")
    print(f"Using URL: {url}")
    response = requests.get(url)
    print(f"Geocoding response status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Geocoding data: {data}")
        if data.get("results"):
            result = data["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            print(f"Found coordinates: {lat}, {lon}")
            return str(lat), str(lon)
    print("Could not find coordinates")
    return None, None


def get_weather(location, datetime_str=None):
    print(f"\nGetting weather for: {location} at {datetime_str}")
    lat, lon = get_coordinates(location)
    if lat is None or lon is None:
        print(f"Could not find coordinates for location: {location}")
        return None

    # Weather codes mapping
    weather_codes = {
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
    }

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,windspeed_10m,cloudcover,precipitation_probability"
        f"&timezone=Europe/Warsaw"
    )

    if datetime_str:
        # Extract date from datetime string (format: YYYY-MM-DDTHH:mm)
        date = datetime_str.split("T")[0]
        url += f"&start_date={date}&end_date={date}"

    print(f"Requesting weather data from: {url}")
    try:
        response = requests.get(url)
        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if "hourly" in data and "time" in data["hourly"]:
                hourly = data["hourly"]
                time_index = None

                # If datetime is provided, find the closest time index
                if datetime_str:
                    times = hourly["time"]
                    for i, time in enumerate(times):
                        if time >= datetime_str:
                            time_index = i
                            break
                    if (
                        time_index is None and times
                    ):  # If no future time found, use the last available
                        time_index = len(times) - 1
                else:
                    # If no datetime provided, use the most recent data
                    time_index = len(hourly["time"]) - 1

                if time_index is not None:
                    print(f"Using weather data for time: {hourly['time'][time_index]}")

                    temp = hourly["temperature_2m"][time_index]
                    wind = hourly["windspeed_10m"][time_index]
                    cloud = hourly["cloudcover"][time_index]
                    rain_prob = hourly["precipitation_probability"][time_index]

                    weather_data = {
                        "temp-c": f"{temp}°C",
                        "wind-kph": f"{wind} km/h",
                        "cloud": f"{cloud}%",
                        "rain": "Tak" if rain_prob > 50 else "Nie",
                    }

                    print(f"Weather data: {weather_data}")
                    return weather_data

            print("No valid hourly data found in response")
        else:
            print(f"Error response from API: {response.status_code}")
    except Exception as e:
        print(f"Exception while fetching weather data: {e}")

    return None


def get_air_quality_metrics(location, datetime_str=None):
    print(f"\nGetting air quality metrics for: {location} at {datetime_str}")
    lat, lon = get_coordinates(location)
    if lat is None or lon is None:
        print(f"Could not find coordinates for location: {location}")
        return [0, 0, 0, 0]  # Return default values if coordinates not found

    url = (
        f"{OPENMETO_BASE_URL}v1/air-quality"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide"
        f"&timezone=Europe/Warsaw"
    )

    if datetime_str:
        # Extract date from datetime string (format: YYYY-MM-DDTHH:mm)
        date = datetime_str.split("T")[0]
        url += f"&start_date={date}&end_date={date}"

    print(f"Requesting air quality data from: {url}")
    try:
        response = requests.get(url)
        print(f"Response status: {response.status_code}")
        print(
            f"Response text: {response.text[:500]}"
        )  # Print first 500 chars of response

        if response.status_code == 200:
            data = response.json()
            if "hourly" in data and "time" in data["hourly"]:
                hourly = data["hourly"]
                time_index = None

                # If datetime is provided, find the closest time index
                if datetime_str:
                    times = hourly["time"]
                    for i, time in enumerate(times):
                        if time >= datetime_str:
                            time_index = i
                            break
                    if (
                        time_index is None and times
                    ):  # If no future time found, use the last available
                        time_index = len(times) - 1
                else:
                    # If no datetime provided, use the most recent data
                    time_index = len(hourly["time"]) - 1

                if time_index is not None:
                    print(f"Using data for time: {hourly['time'][time_index]}")
                    current_pm10 = hourly.get("pm10", [0])[time_index] or 0
                    current_pm2_5 = hourly.get("pm2_5", [0])[time_index] or 0
                    current_carbon_monoxide = (
                        hourly.get("carbon_monoxide", [0])[time_index] or 0
                    )
                    current_nitrogen_dioxide = (
                        hourly.get("nitrogen_dioxide", [0])[time_index] or 0
                    )

                    print(
                        f"Values: PM10={current_pm10}, PM2.5={current_pm2_5}, CO={current_carbon_monoxide}, NO2={current_nitrogen_dioxide}"
                    )
                    return [
                        current_pm10,
                        current_pm2_5,
                        current_carbon_monoxide,
                        current_nitrogen_dioxide,
                    ]

            print("No valid hourly data found in response")
        else:
            print(f"Error response from API: {response.status_code}")
    except Exception as e:
        print(f"Exception while fetching air quality data: {e}")

    return [0, 0, 0, 0]  # Return default values if data cannot be fetched
