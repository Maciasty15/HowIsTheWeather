"""Plik odpowiada za ładowanie danych do konfiguracji z .env (klucze do API itp)"""

from dotenv import load_dotenv
import os

load_dotenv()
WEATHERAPI_API_KEY = os.getenv("WEATHERAPI_API_KEY")

# DEBUG
print(WEATHERAPI_API_KEY)
