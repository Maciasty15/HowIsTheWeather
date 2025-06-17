import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import ctx

app = dash.Dash(__name__)

city_ids = ["btn-warszawa", "btn-wrocław", "btn-poznań", "btn-kraków", "btn-gdańsk", "btn-szczecin"]
city_names = ["Warszawa", "Wrocław", "Poznań", "Kraków", "Gdańsk", "Szczecin"]

app.layout = html.Div([
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
    html.Div("Podpowiedź z Gemini", className="ai-suggestion-box")
])

@app.callback(
    Output("selected-city", "children"),
    [Input(btn_id, "n_clicks") for btn_id in city_ids]
)
def show_selected_city(*args):
    triggered = ctx.triggered_id
    city_map = dict(zip(city_ids, city_names))
    city = city_map.get(triggered, None)
    if city:
        print(f"[INFO] Wybrano miasto: {city}")
    return f"Wybrane miasto: {city}" if city else ""f"Wybrane miasto: {city}" if city else ""

@app.callback(
    Output("confirmed-datetime", "children"),
    Input("confirm-time", "n_clicks"),
    State("date-picker", "date"),
    State("hour-input", "value"),
    State("minute-input", "value")
)
def show_confirmed_datetime(n_clicks, date, hour, minute):
    if n_clicks:
        h = f"{int(hour):02d}" if hour is not None else "--"
        m = f"{int(minute):02d}" if minute is not None else "--"
        print(f"[INFO] Wybrano datę i godzinę: {date} {h}:{m}")
        return f"Wybrana data i godzina: {date} {h}:{m}"
    return ""f"Wybrana data i godzina: {date} {h}:{m}"
    return ""

if __name__ == '__main__':
    app.run(debug=True)
