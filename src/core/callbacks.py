# src/core/callbacks.py
from dash import Input, Output, State, ctx
from src.services.open_meteo_api import get_weather, get_air_quality_metrics
from src.services.recommender import get_recommendation
from src.core.constants import city_ids, city_names


def register_callbacks(app):
    @app.callback(
        [Output("selected-city", "children"), Output("store-city", "data")],
        [Input(btn_id, "n_clicks") for btn_id in city_ids],
    )
    def show_selected_city(*args):
        triggered = ctx.triggered_id
        city_map = dict(zip(city_ids, city_names))
        city = city_map.get(triggered, None) if triggered else None
        if city:
            return f"Wybrane miasto: {city}", {"city": city}
        return "", {}

    @app.callback(
        [Output("confirmed-datetime", "children"), Output("store-datetime", "data")],
        Input("confirm-time", "n_clicks"),
        State("date-picker", "date"),
        State("hour-input", "value"),
        State("minute-input", "value"),
    )
    def show_confirmed_datetime(n_clicks, date, hour, minute):
        if not n_clicks or not all([date, hour is not None, minute is not None]):
            return "Proszę wybrać datę i godzinę", None
        h, m = f"{int(hour):02d}", f"{int(minute):02d}"
        return f"Wybrana data i godzina: {date} {h}:{m}", f"{date}T{h}:{m}"

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

        location = selected_city.get("city", "nieznana lokalizacja")
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
