import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import ctx
from weatherapi import get_air_quality_metrics

app = dash.Dash(__name__)

# Przechowywanie danych testowych
app.layout_store = dcc.Store(id="store-weather", data={})
app.layout_air = dcc.Store(id="store-air", data={})
app.layout_ai = dcc.Store(id="store-gemini", data="")
app.layout_city = dcc.Store(id="store-city", data="")  # New store for selected city
app.layout_datetime = dcc.Store(id="store-datetime", data="")  # Store for selected datetime

city_ids = ["btn-warszawa", "btn-wrocław", "btn-poznań", "btn-kraków", "btn-gdańsk", "btn-szczecin"]
city_names = ["Warszawa", "Wrocław", "Poznań", "Kraków", "Gdańsk", "Szczecin"]

app.layout = html.Div([
    app.layout_store,
    app.layout_air,
    app.layout_ai,
    app.layout_city,  # Add the city store to the layout
    app.layout_datetime,  # Add the datetime store to the layout
    html.H1("HowIsTheWeather", className="title"),

    html.P("""
    Nasza aplikacja pozwoli ci:
    - sprawdzić aktualną pogodę
    - sprawdzić aktualne zanieczyszczenie powietrza
    - doradzić Ci w kwestii aktywności fizycznej
    - doradzić Ci w kwestii doboru odpowiedniej odzieży
    """, className="intro-text"),

    html.H2("Wybierz miasto", className="section-title"),
    html.Div([
        html.Button(city, id=btn_id, className="city-button")
        for city, btn_id in zip(city_names, city_ids)
    ], className="city-button-container"),

    html.Div(id="selected-city", style={"marginTop": "10px", "textAlign": "center"}),

    html.Br(),

    html.Div([
        html.P("Wybierz datę i godzinę", className="section-title"),
        dcc.DatePickerSingle(
            id='date-picker',
            date='2025-06-16',
            className="date-picker"
        ),
        html.Div([
            dcc.Input(
                id='hour-input',
                type='number',
                placeholder='HH',
                min=0,
                max=23,
                className="time-input"
            ),
            dcc.Input(
                id='minute-input',
                type='number',
                placeholder='MM',
                min=0,
                max=59,
                className="time-input"
            ),
            html.Button("Zatwierdź datę i czas", id="confirm-time", className="confirm-button")
        ], className="time-input-group")
    ], className="datetime-section"),

    html.Div(id="confirmed-datetime", style={"marginTop": "10px", "textAlign": "center"}),

    html.H2("Twoja Prognoza Pogody", className="section-title"),
    html.Div([
        html.Div([html.Span("Temperatura", className="label"), html.Span(id="temp-c", children="--", className="value")], className="row"),
        html.Div([html.Span("Wiatr", className="label"), html.Span(id="wind-kph", children="--", className="value")], className="row"),
        html.Div([html.Span("Zachmurzenie", className="label"), html.Span(id="cloud", children="--", className="value")], className="row"),
        html.Div([html.Span("Szansa na deszcz", className="label"), html.Span(id="rain", children="--", className="value")], className="row")
    ], className="forecast-box"),

    html.H2("Jakość powietrza na dzień prognozy", className="section-title"),
    html.Div([
        html.Div([html.Span("Tlenek Węgla w ug/m3", className="label"), html.Span(id="air-co", children="--", className="value")], className="row"),
        html.Div([html.Span("Dwutlenek Azotu ug/m3", className="label"), html.Span(id="air-no2", children="--", className="value")], className="row"),
        html.Div([html.Span("Pyły zawieszone PM2.5 ug/m3", className="label"), html.Span(id="air-pm2_5", children="--", className="value")], className="row"),
        html.Div([html.Span("Pyły zawieszone PM10 ug/m3", className="label"), html.Span(id="air-pm10", children="--", className="value")], className="row")
    ], className="air-quality-box"),

    html.Br(),
    html.H2("Zalecenia asystenta AI co do ubioru i aktywności", className="section-title"),
    html.Div(id="ai-suggestion-box", children="Podpowiedź z Gemini", className="ai-suggestion-box")
])

@app.callback(
    [Output("selected-city", "children"),
     Output("store-city", "data")],
    [Input(btn_id, "n_clicks") for btn_id in city_ids]
)
# TODO: Tutaj dodaj połączenie z klasą API, która pobierze dane pogodowe i jakości powietrza na podstawie miasta
    # Przykład:
    # from services.weatherapi import WeatherFetcher
    # weather_data, air_data = WeatherFetcher().fetch_by_city(city)
    # return odpowiednia_logika_ustawiania_danych

def show_selected_city(*args):
    triggered = ctx.triggered_id
    city_map = dict(zip(city_ids, city_names))
    city = city_map.get(triggered, None)
    if city:
        print(f"[INFO] Wybrano miasto: {city}")
    return f"Wybrane miasto: {city}" if city else "", city if city else ""

@app.callback(
    [Output("confirmed-datetime", "children"),
     Output("store-datetime", "data")],
    Input("confirm-time", "n_clicks"),
    State("date-picker", "date"),
    State("hour-input", "value"),
    State("minute-input", "value")
)
def show_confirmed_datetime(n_clicks, date, hour, minute):
    if not n_clicks:  # Initial load or reset
        return "", None
        
    if not all([date, hour is not None, minute is not None]):  # If any value is missing
        return "Proszę wybrać datę i godzinę", None
        
    h = f"{int(hour):02d}"
    m = f"{int(minute):02d}"
    datetime_str = f"{date}T{h}:{m}"
    print(f"[INFO] Wybrano datę i godzinę: {datetime_str}")
    return f"Wybrana data i godzina: {date} {h}:{m}", datetime_str

@app.callback(
    [
        Output("temp-c", "children"),
        Output("wind-kph", "children"),
        Output("cloud", "children"),
        Output("rain", "children")
    ],
    [Input("store-city", "data"),
     Input("store-datetime", "data")]
)
def update_weather_ui(selected_city, selected_datetime):
    if not selected_city:  # Only check if city is not selected
        return "--", "--", "--", "--"
    
    from weatherapi import get_weather
    # Pass datetime only if it's selected, otherwise get current values
    weather_data = get_weather(selected_city, selected_datetime if selected_datetime else None)
    
    if weather_data is None:
        return "--", "--", "--", "--"
        
    return (
        weather_data.get("temp-c", "--"),
        weather_data.get("wind-kph", "--"),
        weather_data.get("cloud", "--"),
        weather_data.get("rain", "--")
    )


@app.callback(
    [
        Output("air-co", "children"),
        Output("air-no2", "children"),
        Output("air-pm2_5", "children"),
        Output("air-pm10", "children")
    ],
    [Input("store-city", "data"),
     Input("store-datetime", "data")]
)
def update_air_ui(selected_city, selected_datetime):
    if not selected_city:  # Only check if city is not selected
        return "--", "--", "--", "--"
        
    # Pass datetime only if it's selected, otherwise get current values
    df = get_air_quality_metrics(selected_city, selected_datetime if selected_datetime else None)
    return df[2], df[3], df[1], df[0]


@app.callback(
    Output("ai-suggestion-box", "children"),
    Input("store-gemini", "data")
)
def update_ai_text(text):
    return text or "Podpowiedź z Gemini"

if __name__ == '__main__':
    app.run(debug=True)
