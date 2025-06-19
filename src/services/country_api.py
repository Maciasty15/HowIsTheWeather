import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEOCODING_BASE_URL = os.getenv("GEOCODING_BASE_URL")


def get_countries(language="pl"):
    url = f"{GEOCODING_BASE_URL}countries?format=json&language={language}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            return [{"label": c["name"], "value": c["name"]} for c in data["results"]]
    return []
