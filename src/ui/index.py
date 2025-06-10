import dash
from dash import html, dcc, Input, Output, State

from src.services.weatherapi import get_weather
from src.core.recommender import get_recommendation

app = dash.Dash(__name__)
app.title = "Rekomendacje na podstawie pogody"

app.layout = html.Div([
    html.H1("Podaj lokalizację, a podpowiemy Ci co robić i jak się ubrać!"),
    dcc.Input(id='location-input', type='text', placeholder='np. Warszawa', style={'width': '300px'}),
    html.Button('Sprawdź', id='submit-button', n_clicks=0),
    html.Div(id='weather-output', style={'marginTop': '20px', 'fontSize': '18px'}),
    html.Div(id='recommendation-output', style={'marginTop': '20px', 'fontSize': '18px', 'whiteSpace': 'pre-wrap'})
])

@app.callback(
    Output('weather-output', 'children'),
    Output('recommendation-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('location-input', 'value')
)
def update_output(n_clicks, location):
    if n_clicks > 0 and location:
        weather_description = get_weather(location)
        if "Nie udało się pobrać pogody" in weather_description:
            return weather_description, ""
        
        print(weather_description)

        recommendation = get_recommendation(location, weather_description)

        print(recommendation)

        return f"Pogoda w {location}: {weather_description}", recommendation
    return "", ""

# Funkcja do uruchamiania serwera
def run():
    app.run(debug=True)