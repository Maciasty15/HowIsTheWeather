import os
import redis
import json
from datetime import timedelta
from typing import Optional

# === Konfiguracja Redis ===
try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=0,
        decode_responses=True,
    )
    redis_client.ping()
except redis.ConnectionError:
    print("[ERROR] Redis niedostępny")
    redis_client = None

# === TTL (czas życia cache) ===
WEATHER_TTL = timedelta(minutes=5)
AIR_TTL = timedelta(minutes=10)


# === Pogoda: cache + API fallback ===
def get_weather(city: str, datetime_str: Optional[str] = None):
    from src.services.weatherapi import get_weather as get_weather_from_api

    key = f"weather:{city.lower()}:{datetime_str if datetime_str else 'now'}"
    if redis_client:
        cached = redis_client.get(key)
        if cached:
            print(f"[CACHE] Pogoda: {city}")
            return json.loads(cached)

    print(f"[API] Pogoda: {city}")
    data = get_weather_from_api(city, datetime_str)
    if redis_client:
        redis_client.setex(key, WEATHER_TTL, json.dumps(data))
    return data


# === Jakość powietrza: cache + API fallback ===
def get_air_quality_metrics(city: str, datetime_str: Optional[str] = None):
    from src.services.weatherapi import (
        get_air_quality_metrics as get_air_quality_metrics_from_api,
    )

    key = f"air:{city.lower()}:{datetime_str if datetime_str else 'now'}"
    if redis_client:
        cached = redis_client.get(key)
        if cached:
            print(f"[CACHE] Powietrze: {city}")
            return json.loads(cached)

    print(f"[API] Powietrze: {city}")
    data = get_air_quality_metrics_from_api(city, datetime_str)
    if redis_client:
        redis_client.setex(key, AIR_TTL, json.dumps(data))
    return data
