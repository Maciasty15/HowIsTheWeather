import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

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
        html.Button(city, id=f"btn-{city.lower()}", className="city-button")
        for city in ["Warszawa", "Wrocław", "Poznań", "Kraków", "Gdańsk", "Szczecin"]
    ], className="city-button-container"),

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
            )
        ], className="time-input-group")
    ], className="datetime-section"),

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
    Output("temp-c", "children"),
    Output("wind-kph", "children"),
    Output("cloud", "children"),
    Output("rain", "children"),
    Output("air-co", "children"),
    Output("air-no2", "children"),
    Output("air-pm2_5", "children"),
    Output("air-pm10", "children"),
    Input("btn-warszawa", "n_clicks"),
    Input("btn-wrocław", "n_clicks"),
    Input("btn-poznań", "n_clicks"),
    Input("btn-kraków", "n_clicks"),
    Input("btn-gdańsk", "n_clicks"),
    Input("btn-szczecin", "n_clicks"),
    State("date-picker", "date"),
    State("hour-input", "value"),
    State("minute-input", "value")
)
def update_forecast(*args):
    # Tu będzie logika np. pobrania z API na podstawie args[-3:] (data, godzina, minuta)
    return [
        "222.4°C",
        "12.5 km/h",
        "40%",
        "Tak",
        "0.33",
        "18.2",
        "10.1",
        "20.4"
    ]

if __name__ == '__main__':
    app.run(debug=True)
