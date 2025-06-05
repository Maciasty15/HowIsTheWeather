"""Moduł obsługujący zapytania do API pogodowego.

Zawiera funkcje odpowiedzialne za:
- budowanie zapytań do API
- wykonywanie żądań HTTP
- parsowanie odpowiedzi

https://www.weatherapi.com/

"""

import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Inicjalizacja zmiennych środowiskowych
load_dotenv()

# Stałe API
API_KEY = os.getenv("WEATHERAPI_API_KEY")
BASE_URL = os.getenv("WEATHERAPI_API_BASE_URL")  # do uzupełnienia

# Opcjonalnie logger (można aktywować, gdy gotowy)
# from src.utils.logger import get_logger
# logger = get_logger(__name__)


def build_query(city: str, **kwargs) -> Dict[str, str]:
    """
    Buduje parametry zapytania do API pogodowego.
    """
    pass  # TODO


def fetch_weather(city: str) -> Optional[Dict[str, Any]]:
    """
    Wysyła zapytanie do API pogodowego i zwraca dane w formacie JSON.
    """
    pass  # TODO


def parse_weather(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parsuje odpowiedź z API i wyciąga kluczowe informacje pogodowe.
    """
    pass  # TODO
