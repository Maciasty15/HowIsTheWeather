import os
import requests
import urllib.parse
from dotenv import load_dotenv

# Inicjalizacja zmiennych środowiskowych
load_dotenv()

# Stałe API
AIR_QUALITY_BASE_URL = os.getenv("AIR_QUALITY_BASE_URL")
GEOCODING_BASE_URL = os.getenv("GEOCODING_BASE_URL")
OPEN_METEO_BASE_URL = os.getenv("OPEN_METEO_BASE_URL")


def get_coordinates(location) -> list[dict[str, str]] | None:
    print(f"Original location name: {location}")

    # Encode the location name properly for URL
    encoded_location = urllib.parse.quote(location)
    print(f"URL-encoded location name: {encoded_location}")

    # First try with language=pl
    url = f"{GEOCODING_BASE_URL}search?name={encoded_location}&count=10&format=json&language=pl"
    print(f"Searching coordinates for location: {location} (with language=pl)")
    print(f"Using URL: {url}")
    response = requests.get(url)
    print(f"Geocoding response status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Geocoding data: {data}")
        if data.get("results"):
            results = []
            for result in data["results"]:
                lat = result["latitude"]
                lon = result["longitude"]
                country = result.get("country", "")
                state = result.get("admin1", "")
                results.append(
                    {
                        "lat": str(lat),
                        "lon": str(lon),
                        "country": country,
                        "state": state,
                        "name": result.get("name", location),
                    }
                )
            if results:
                return results
    # Fallback: try without language param
    url = f"{GEOCODING_BASE_URL}search?name={encoded_location}&count=10&format=json"
    print(f"Fallback: Searching coordinates for location: {location} (no language)")
    print(f"Using URL: {url}")
    response = requests.get(url)
    print(f"Geocoding response status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Geocoding data: {data}")
        if data.get("results"):
            results = []
            for result in data["results"]:
                lat = result["latitude"]
                lon = result["longitude"]
                country = result.get("country", "")
                state = result.get("admin1", "")
                results.append(
                    {
                        "lat": str(lat),
                        "lon": str(lon),
                        "country": country,
                        "state": state,
                        "name": result.get("name", location),
                    }
                )
            if results:
                return results
    print("Could not find coordinates")
    return None


def get_weather(location, datetime_str=None):
    print(f"\nGetting weather for: {location} at {datetime_str}")
    # Accept both city name (str) and dict with lat/lon
    if isinstance(location, dict) and "lat" in location and "lon" in location:
        lat = location["lat"]
        lon = location["lon"]
    else:
        coordinates = get_coordinates(location)
        if (
            coordinates is None
            or not isinstance(coordinates, list)
            or len(coordinates) == 0
        ):
            print(f"Could not find coordinates for location: {location}")
            return None
        lat = coordinates[0]["lat"]
        lon = coordinates[0]["lon"]

    url = (
        f"{OPEN_METEO_BASE_URL}forecast"
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
    # Accept both city name (str) and dict with lat/lon
    if isinstance(location, dict) and "lat" in location and "lon" in location:
        lat = location["lat"]
        lon = location["lon"]
    else:
        coordinates = get_coordinates(location)
        if (
            coordinates is None
            or not isinstance(coordinates, list)
            or len(coordinates) == 0
        ):
            print(f"Could not find coordinates for location: {location}")
            return [0, 0, 0, 0]  # Return default values if coordinates not found
        lat = coordinates[0]["lat"]
        lon = coordinates[0]["lon"]

    url = (
        f"{AIR_QUALITY_BASE_URL}/air-quality"
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
