from services.weatherapi import get_coordinates, get_weather, get_air_quality_metrics
import os
from dotenv import load_dotenv
from unittest.mock import patch, Mock

load_dotenv()
OPENMETO_BASE_URL = os.getenv("WEATHERAPI_API_BASE_URL")


class TestGetCoordinates:
    @patch("requests.get")
    def test_get_coordinates_success(self, mock_get):
        # arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"latitude": "52.23", "longitude": "21.01"}]
        }
        mock_get.return_value = mock_response

        # act
        lat, lon = get_coordinates("Warszawa")

        # assert
        assert lat == "52.23"
        assert lon == "21.01"
        mock_get.assert_called_once_with(
            f"{OPENMETO_BASE_URL}search?name=Warszawa&count=1&language=pl&format=json"
        )

    @patch("requests.get")
    def test_get_coordinates_no_results(self, mock_get):
        # arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        # act
        lat, lon = get_coordinates("Nieistniejące Miasto")

        # assert
        assert lat is None
        assert lon is None

    @patch("requests.get")
    def test_get_coordinates_api_error(self, mock_get):
        # arrange
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # act
        lat, lon = get_coordinates("Warszawa")

        # assert
        assert lat is None
        assert lon is None


class TestGetWeather:
    @patch("services.weatherapi.get_coordinates")
    @patch("requests.get")
    def test_get_weather_success(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current_weather": {
                "temperature": 15.5,
                "windspeed": 10.2,
                "weathercode": 2,
            }
        }
        mock_get.return_value = mock_response

        # act
        result = get_weather("Warszawa")

        # assert
        assert "Częściowe zachmurzenie" in result
        assert "temperatura: 15.5°C" in result
        assert "wiatr: 10.2 km/h" in result
        mock_get.assert_called_once_with(
            f"{OPENMETO_BASE_URL}forecast?latitude=52.23&longitude=21.01&current_weather=true"
        )

    @patch("services.weatherapi.get_coordinates")
    def test_get_weather_invalid_coordinates(self, mock_get_coords):
        # arrange
        mock_get_coords.return_value = (None, None)

        # act
        result = get_weather("Nieistniejące Miasto")

        # assert
        assert "Nie udało się znaleźć współrzędnych" in result

    @patch("services.weatherapi.get_coordinates")
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
        assert "Błąd przy pobieraniu danych pogodowych" in result

    @patch("services.weatherapi.get_coordinates")
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
        assert "Nie udało się pobrać danych pogodowych" in result

    @patch("services.weatherapi.get_coordinates")
    @patch("requests.get")
    def test_get_weather_unknown_weather_code(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current_weather": {
                "temperature": 15.5,
                "windspeed": 10.2,
                "weathercode": 999,  # nieznany kod
            }
        }
        mock_get.return_value = mock_response

        # act
        result = get_weather("Warszawa")

        # assert
        assert "Nieznana pogoda" in result


class TestGetAirQuality:
    @patch("services.weatherapi.get_coordinates")
    @patch("requests.get")
    def test_get_air_quality_metrics_success(self, mock_get, mock_get_coords):
        # arrange
        mock_get_coords.return_value = ("52.23", "21.01")

        mock_response = Mock()
        mock_response.status_code = 200
        mock_current = Mock()
        mock_variable = Mock()
        mock_variable.Value.side_effect = [25.0, 15.0, 500.0, 40.0]  # PM10, PM2.5, CO, NO2
        mock_current.Variables.return_value = mock_variable
        mock_response.Current.return_value = mock_current
        mock_get.return_value = mock_response

        # act
        result = get_air_quality_metrics("Warszawa")

        # assert
        assert "Tlenek węgla: 500.0 µg/m³" in result
        assert "Dwutlenek Azotu: 40.0 µg/m³" in result
        assert "Pyły zawieszone PM2.5: 15.0 µg/m³" in result
        assert "Pyły zawieszone PM10: 25.0 µg/m³" in result
        mock_get.assert_called_once_with(
            f"{OPENMETO_BASE_URL}air-quality?latitude=52.23&longitude=21.01&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide"
        )

    @patch("services.weatherapi.get_coordinates")
    def test_get_air_quality_metrics_invalid_coordinates(self, mock_get_coords):
        # arrange
        mock_get_coords.return_value = (None, None)

        # act
        result = get_air_quality_metrics("Nieistniejące Miasto")

        # assert
        assert "Nie udało się znaleźć współrzędnych" in result

    @patch("services.weatherapi.get_coordinates")
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
        assert "Nie udało się pobrać danych pogodowych" in result
