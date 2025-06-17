import dash
from dash import html, dcc

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
        html.Div([html.Span("Temperatura", className="label"), html.Span(id="temp-c", children="26.3 °C", className="value")], className="row"),
        html.Div([html.Span("Wiatr", className="label"), html.Span(id="wind-kph", children="6.8 km/h", className="value")], className="row"),
        html.Div([html.Span("Zachmurzenie", className="label"), html.Span(id="cloud", children="0%", className="value")], className="row"),
        html.Div([html.Span("Szansa na deszcz", className="label"), html.Span(id="rain", children="Nie", className="value")], className="row")
    ], className="forecast-box"),

    html.H2("Jakość powietrza na dzień prognozy", className="section-title"),
    html.Div([
        html.Div([html.P("Dwutlenek Węgla w ug/m3"), html.Div('"air_quality": co')]),
        html.Div([html.P("Dwutlenek Azotu ug/m3"), html.Div('"air_quality": no2')]),
        html.Div([html.P("Pyły zawieszone PM2.5 ug/m3"), html.Div('"air_quality": pm2_5')]),
        html.Div([html.P("Pyły zawieszone PM10 ug/m3"), html.Div('"air_quality": pm10')])
    ], className="air-quality-box"),

    html.Br(),
    html.H2("Zalecenia asystenta AI co do ubioru i aktywności", className="section-title"),
    html.Div("Podpowiedź z Gemini", className="ai-suggestion-box")
])

if __name__ == '__main__':
    app.run(debug=True)
