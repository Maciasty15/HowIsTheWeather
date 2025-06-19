# src/core/callbacks.py
from dash import Input, Output, State, ctx, html, ALL
from src.services.open_meteo_api import (
    get_weather,
    get_air_quality_metrics,
    get_coordinates,
)
from src.services.recommender import get_recommendation
from src.services.country_api import get_countries
import json
import re


def register_callbacks(app):
    @app.callback(
        Output("country-dropdown", "options"),
        Input("country-dropdown", "search_value"),
        prevent_initial_call=True,
    )
    def update_country_options(search_value):
        countries = [
            {"label": "Austria", "value": "Austria"},
            {"label": "Belgia", "value": "Belgia"},
            {"label": "Bułgaria", "value": "Bułgaria"},
            {"label": "Chorwacja", "value": "Chorwacja"},
            {"label": "Cypr", "value": "Cypr"},
            {"label": "Czechy", "value": "Czechy"},
            {"label": "Dania", "value": "Dania"},
            {"label": "Estonia", "value": "Estonia"},
            {"label": "Finlandia", "value": "Finlandia"},
            {"label": "Francja", "value": "Francja"},
            {"label": "Grecja", "value": "Grecja"},
            {"label": "Hiszpania", "value": "Hiszpania"},
            {"label": "Holandia", "value": "Holandia"},
            {"label": "Irlandia", "value": "Irlandia"},
            {"label": "Litwa", "value": "Litwa"},
            {"label": "Luksemburg", "value": "Luksemburg"},
            {"label": "Łotwa", "value": "Łotwa"},
            {"label": "Malta", "value": "Malta"},
            {"label": "Niemcy", "value": "Niemcy"},
            {"label": "Polska", "value": "Polska"},
            {"label": "Portugalia", "value": "Portugalia"},
            {"label": "Rumunia", "value": "Rumunia"},
            {"label": "Słowacja", "value": "Słowacja"},
            {"label": "Słowenia", "value": "Słowenia"},
            {"label": "Szwecja", "value": "Szwecja"},
            {"label": "Węgry", "value": "Węgry"},
            {"label": "Włochy", "value": "Włochy"},
        ]
        if search_value:
            return [c for c in countries if search_value.lower() in c["label"].lower()]
        return countries

    @app.callback(
        Output("city-dropdown", "options"),
        [
            Input("city-dropdown", "search_value"),
            Input("country-dropdown", "value"),
            Input("last-selected-city", "data"),
        ],
        State("city-dropdown", "value"),
        prevent_initial_call=True,
    )
    def update_city_options(search_value, country, last_selected, current_value):
        options = []
        if country and search_value and len(search_value) >= 2:
            matches = get_coordinates(f"{search_value}, {country}")
            if matches is None:
                matches = []
            options = [
                {
                    "label": f"{m['name']} (City), {m['state']} (State), {m['country']} (Country)",
                    "value": json.dumps(m),
                }
                for m in matches
            ]
        # Always include the last selected city if not present
        if last_selected and last_selected not in [opt["value"] for opt in options]:
            city = json.loads(last_selected)
            options.append(
                {
                    "label": f"{city['name']} (City), {city['state']} (State), {city['country']} (Country)",
                    "value": last_selected,
                }
            )
        # Also include the current value if not present
        if current_value and current_value not in [opt["value"] for opt in options]:
            city = json.loads(current_value)
            options.append(
                {
                    "label": f"{city['name']} (City), {city['state']} (State), {city['country']} (Country)",
                    "value": current_value,
                }
            )
        return options

    @app.callback(
        [Output("confirmed-datetime", "children"), Output("store-datetime", "data")],
        [
            Input("date-picker", "date"),
            Input("hour-input", "value"),
            Input("minute-input", "value"),
        ],
    )
    def show_confirmed_datetime(date, hour, minute):
        if not all([date, hour is not None, minute is not None]):
            return "Proszę wybrać datę i godzinę", None
        h, m = f"{int(hour):02d}", f"{int(minute):02d}"
        date_str = str(date)
        if "T" in date_str:
            date_part = date_str.split("T")[0]
        else:
            date_part = date_str
        return f"{date_part} {h}:{m}", f"{date_part}T{h}:{m}"

    @app.callback(
        [
            Output("temp-c", "children"),
            Output("wind-kph", "children"),
            Output("cloud", "children"),
            Output("rain", "children"),
            Output("store-weather", "data"),
        ],
        [Input("store-city", "data"), Input("store-datetime", "data")],
    )
    def update_weather_ui(selected_city, selected_datetime):
        if not selected_city:
            return "--", "--", "--", "--", {}
        city = selected_city.get("city", selected_city)
        weather_data = get_weather(city, selected_datetime or None)
        if not weather_data:
            return "--", "--", "--", "--", {}
        return (
            weather_data.get("temp-c", "--"),
            weather_data.get("wind-kph", "--"),
            weather_data.get("cloud", "--"),
            weather_data.get("rain", "--"),
            weather_data,
        )

    @app.callback(
        [
            Output("air-co", "children"),
            Output("air-no2", "children"),
            Output("air-pm2_5", "children"),
            Output("air-pm10", "children"),
            Output("store-air", "data"),
        ],
        [Input("store-city", "data"), Input("store-datetime", "data")],
    )
    def update_air_ui(selected_city, selected_datetime):
        if not selected_city:
            return "--", "--", "--", "--", {}
        # If selected_city is a dict with lat/lon, pass the full dict to get_air_quality_metrics
        if (
            isinstance(selected_city, dict)
            and "lat" in selected_city
            and "lon" in selected_city
        ):
            df = get_air_quality_metrics(selected_city, selected_datetime or None)
        else:
            city = selected_city.get("city", selected_city)
            df = get_air_quality_metrics(city, selected_datetime or None)
        air_data = {"pm10": df[0], "pm2_5": df[1], "co": df[2], "no2": df[3]}
        return df[2], df[3], df[1], df[0], air_data

    @app.callback(
        Output("ai-suggestion-box", "children"),
        [
            Input("store-weather", "data"),
            Input("store-city", "data"),
            Input("store-air", "data"),
        ],
    )
    def generate_ai_recommendation(weather_data, selected_city, air_data):
        if not weather_data or not selected_city:
            return "Podpowiedź z Gemini - może zająć chwilę po wyświetleniu danych pogodowych"

        # Use full city info if available
        if isinstance(selected_city, dict):
            location = f"{selected_city.get('name', '')}, {selected_city.get('country', '')}, {selected_city.get('state', '')}".strip(
                ", "
            )
            if not selected_city.get("name"):
                location = "nieznana lokalizacja"
        else:
            location = selected_city or "nieznana lokalizacja"

        weather_parts = [
            f"Temperatura: {weather_data.get('temp-c', '--')}\u00b0C",
            f"Wiatr: {weather_data.get('wind-kph', '--')} km/h",
            f"Zachmurzenie: {weather_data.get('cloud', '--')}%",
            f"Szansa na deszcz: {weather_data.get('rain', '--')}%",
        ]
        air_parts = (
            [
                f"PM2.5: {air_data.get('pm2_5', '--')} µg/m3",
                f"PM10: {air_data.get('pm10', '--')} µg/m3",
                f"NO2: {air_data.get('no2', '--')} µg/m3",
                f"CO: {air_data.get('co', '--')} µg/m3",
            ]
            if isinstance(air_data, dict)
            else ["Brak danych o jakości powietrza."]
        )

        full_description = "\n".join(weather_parts + [""] + air_parts)
        return get_recommendation(location, full_description)

    @app.callback(
        [
            Output("city-dropdown", "value"),
            Output("store-city", "data"),
            Output("last-selected-city", "data"),
        ],
        [Input("country-dropdown", "value"), Input("city-dropdown", "value")],
        prevent_initial_call=True,
    )
    def handle_city_and_country_change(country, selected_city_json):
        ctx_trigger = ctx.triggered_id
        if ctx_trigger == "country-dropdown":
            # Country changed: clear city
            return None, {}, None
        elif ctx_trigger == "city-dropdown" and selected_city_json:
            try:
                city = json.loads(selected_city_json)
                return selected_city_json, city, selected_city_json
            except Exception:
                return selected_city_json, {}, selected_city_json
        return None, {}, None
