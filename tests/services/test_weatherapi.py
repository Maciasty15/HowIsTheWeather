from services.open_meteo_api import (
    get_coordinates,
    get_weather,
    get_air_quality_metrics,
)
import os
from dotenv import load_dotenv
import urllib.parse
from unittest.mock import patch, Mock, MagicMock

load_dotenv()
AIR_QUALITY_BASE_URL = os.getenv("AIR_QUALITY_BASE_URL")
GEOCODING_BASE_URL = os.getenv("GEOCODING_BASE_URL")
OPEN_METEO_BASE_URL = os.getenv("OPEN_METEO_BASE_URL")


class TestGetCoordinates:
    @patch("requests.get")
    def test_get_coordinates_success(self, mock_get):
        # arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "latitude": 52.23,
                    "longitude": 21.01,
                    "country": "Polska",
                    "admin1": "Mazowieckie",
                    "name": "Warszawa",
                }
            ]
        }
        mock_get.return_value = mock_response

        location = "Warszawa"
        encoded_location = urllib.parse.quote(location)

        # act
        results = get_coordinates(location)

        # assert
        assert isinstance(results, list)
        assert results[0]["lat"] == "52.23"
        assert results[0]["lon"] == "21.01"
        assert results[0]["country"] == "Polska"
        assert results[0]["state"] == "Mazowieckie"
        assert results[0]["name"] == "Warszawa"

    @patch("requests.get")
    def test_get_coordinates_no_results(self, mock_get):
        # arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        # act
        results = get_coordinates("Nieistniejące Miasto")

        # assert
        assert results is None

    @patch("requests.get")
    def test_get_coordinates_api_error(self, mock_get):
        # arrange
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # act
        results = get_coordinates("Warszawa")

        # assert
        assert results is None


class TestGetWeather:
    @patch("services.open_meteo_api.get_coordinates")
    @patch("requests.get")
    def test_get_weather_success(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "hourly": {
                "time": ["2025-06-18T19:00", "2025-06-18T20:00"],
                "temperature_2m": [14.0, 15.5],
                "windspeed_10m": [8.0, 10.2],
                "cloudcover": [40, 60],
                "precipitation_probability": [10, 30],
            }
        }
        mock_get.return_value = mock_response

        # act
        result = get_weather("Warszawa", "2025-06-18T19:30")

        # assert
        assert result == {
            "temp-c": "15.5°C",
            "wind-kph": "10.2 km/h",
            "cloud": "60%",
            "rain": "Nie",
        }
        assert mock_get.call_count == 1
        called_url = mock_get.call_args[0][0]
        assert "latitude=52.23" in called_url
        assert "longitude=21.01" in called_url
        assert "start_date=2025-06-18" in called_url

    @patch("services.open_meteo_api.get_coordinates")
    def test_get_weather_invalid_coordinates(self, mock_get_coords):
        # arrange
        mock_get_coords.return_value = (None, None)

        # act
        result = get_weather("Nieistniejące Miasto")

        # assert
        assert result is None

    @patch("services.open_meteo_api.get_coordinates")
    @patch("requests.get")
    def test_get_weather_api_error(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # act
        result = get_weather("Warszawa")

        # assert
        assert result is None

    @patch("services.open_meteo_api.get_coordinates")
    @patch("requests.get")
    def test_get_weather_missing_data(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        # act
        result = get_weather("Warszawa")

        # assert
        assert result is None

    @patch("services.open_meteo_api.get_coordinates")
    @patch("requests.get")
    def test_get_weather_edge_rain_probability(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "hourly": {
                "time": ["2025-06-18T10:00"],
                "temperature_2m": [20.0],
                "windspeed_10m": [5.0],
                "cloudcover": [10],
                "precipitation_probability": [60],  # powyżej progu 50%
            }
        }
        mock_get.return_value = mock_response

        # act
        result = get_weather("Warszawa", "2025-06-18T09:00")

        # assert
        assert result == {
            "temp-c": "20.0°C",
            "wind-kph": "5.0 km/h",
            "cloud": "10%",
            "rain": "Tak",
        }


class TestGetAirQuality:
    @patch("services.open_meteo_api.get_coordinates")
    @patch("services.open_meteo_api.requests.get")
    def test_get_air_quality_metrics_success(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "hourly": {
                "time": ["2025-06-18T09:00", "2025-06-18T10:00"],
                "pm10": [22.0, 25.0],
                "pm2_5": [12.0, 15.0],
                "carbon_monoxide": [480.0, 500.0],
                "nitrogen_dioxide": [35.0, 40.0],
            }
        }
        mock_get.return_value = mock_response

        # act
        result = get_air_quality_metrics("Warszawa", "2025-06-18T09:30")

        print(result)

        # assert
        assert result == [25.0, 15.0, 500.0, 40.0]
        mock_get.assert_called_once()
        called_url = mock_get.call_args[0][0]
        assert "latitude=52.23" in called_url
        assert "longitude=21.01" in called_url
        assert "hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide" in called_url
        assert "start_date=2025-06-18" in called_url

    @patch("services.open_meteo_api.get_coordinates")
    def test_get_air_quality_metrics_invalid_coordinates(self, mock_get_coords):
        # arrange
        mock_get_coords.return_value = (None, None)

        # act
        result = get_air_quality_metrics("Nieistniejące Miasto")

        # assert
        assert result == [0, 0, 0, 0]

    @patch("services.open_meteo_api.get_coordinates")
    @patch("requests.get")
    def test_get_air_quality_metrics_api_error(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # act
        result = get_air_quality_metrics("Warszawa")

        # assert
        assert result == [0, 0, 0, 0]

    @patch("services.open_meteo_api.get_coordinates")
    @patch("requests.get")
    def test_get_air_quality_missing_data(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # brak 'hourly'
        mock_get.return_value = mock_response

        # act
        result = get_air_quality_metrics("Warszawa")

        # assert
        assert result == [0, 0, 0, 0]
