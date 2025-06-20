from dash import html, dcc
import datetime


def create_layout():
    now = datetime.datetime.now()

    return html.Div(
        [
            dcc.Store(id="store-weather", data={}),
            dcc.Store(id="store-air", data={}),
            dcc.Store(id="store-gemini", data=""),
            dcc.Store(id="store-city", data=""),
            dcc.Store(id="store-datetime", data=""),
            dcc.Store(id="last-selected-city", data=None),
            html.H1("HowIsTheWeather", className="title"),
            html.P(
                """
    Nasza aplikacja pozwoli Ci:
    🌞 sprawdzić aktualną pogodę
    🌫️ sprawdzić aktualne zanieczyszczenie powietrza
    🏃 doradzić w kwestii aktywności fizycznej
    👕 doradzić w kwestii doboru odpowiedniej odzieży
    """,
                className="intro-text",
            ),
            html.H2("Wybierz miasto 🌆️", className="section-title"),
            html.Div(
                [
                    dcc.Dropdown(
                        id="country-dropdown",
                        options=[],
                        placeholder="Wybierz kraj...",
                        className="country-input",
                        searchable=True,
                        clearable=True,
                        value=None,
                    ),
                    dcc.Dropdown(
                        id="city-dropdown",
                        options=[],
                        placeholder="Wpisz lub wybierz miasto...",
                        className="city-input",
                        searchable=True,
                        clearable=True,
                        optionHeight=40,
                        value=None,
                    ),
                ],
                className="city-input-container",
            ),
            html.Div(
                id="city-matches", style={"marginTop": "10px", "textAlign": "center"}
            ),
            html.Div(
                id="city-matches-list",
                style={"marginTop": "10px", "textAlign": "center"},
            ),
            html.Div(
                id="selected-city", style={"marginTop": "10px", "textAlign": "center"}
            ),
            html.Div(
                [
                    html.P("Wybierz datę i godzinę 🕒", className="section-title"),
                    dcc.DatePickerSingle(
                        id="date-picker",
                        date=now.today(),
                        display_format="YYYY-MM-DD",
                        className="date-picker",
                    ),
                    html.Div(
                        [
                            dcc.Dropdown(
                                id="hour-input",
                                options=[
                                    {"label": f"{h:02d}", "value": h} for h in range(24)
                                ],
                                value=now.hour,
                                clearable=False,
                                className="time-input",
                                style={
                                    "width": "80px",
                                    "display": "inline-block",
                                    "marginRight": "10px",
                                },
                            ),
                            dcc.Dropdown(
                                id="minute-input",
                                options=[
                                    {"label": f"{m:02d}", "value": m}
                                    for m in range(0, 60, 5)
                                ],
                                value=(now.minute // 5) * 5,
                                clearable=False,
                                className="time-input",
                                style={"width": "80px", "display": "inline-block"},
                            ),
                        ],
                        className="time-input-group",
                    ),
                ],
                className="datetime-section",
            ),
            html.Div(
                id="confirmed-datetime",
                style={"marginTop": "10px", "textAlign": "center"},
            ),
            html.H2("Twoja Prognoza Pogody 👇", className="section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("Temperatura 🌡️", className="label"),
                            html.Span(id="temp-c", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Wiatr 💨", className="label"),
                            html.Span(id="wind-kph", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Zachmurzenie ☁️", className="label"),
                            html.Span(id="cloud", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Szansa na deszcz 🌧️", className="label"),
                            html.Span(id="rain", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Wilgotność 💧", className="label"),
                            html.Span(id="humidity", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Indeks UV 🌞", className="label"),
                            html.Span(id="uv-index", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Widoczność 🔭", className="label"),
                            html.Span(
                                id="visibility", children="--", className="value"
                            ),
                        ],
                        className="row",
                    ),
                ],
                className="forecast-box",
            ),
            html.H2("Jakość powietrza na dzień prognozy 👇", className="section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("Tlenek Węgla w ug/m3", className="label"),
                            html.Span(id="air-co", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Dwutlenek Azotu ug/m3", className="label"),
                            html.Span(id="air-no2", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Pyły zawieszone PM2.5 ug/m3", className="label"),
                            html.Span(id="air-pm2_5", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Pyły zawieszone PM10 ug/m3", className="label"),
                            html.Span(id="air-pm10", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Dwutlenek siarki SO₂ ug/m3", className="label"),
                            html.Span(id="air-so2", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Ozon O₃ ug/m3", className="label"),
                            html.Span(id="air-o3", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span(
                                "Indeks Jakości Powietrza (AQI) 📈", className="label"
                            ),
                            html.Span(id="air-aqi", children="--", className="value"),
                        ],
                        className="row",
                    ),
                ],
                className="air-quality-box",
            ),
            html.H2(
                "Zalecenia asystenta AI co do ubioru i aktywności 👇",
                className="section-title",
            ),
            dcc.Markdown(id="ai-suggestion-box", className="ai-suggestion-box"),
            html.H2("Podziel się swoją opinią 📝", className="section-title"),
            html.Div(
                [
                    dcc.Textarea(
                        id="feedback-input",
                        placeholder="Co sądzisz o aplikacji?",
                        style={"width": "100%", "height": 100},
                    ),
                    html.Button("Wyślij opinię", id="submit-feedback", n_clicks=0),
                    html.Div(id="feedback-confirmation", style={"marginTop": "10px"}),
                ],
                className="graph-container",
            ),
            html.Div(
                [
                    html.P("ℹ️ Wskazówki:", className="label"),
                    html.Ul(
                        [
                            html.Li(
                                "Upewnij się, że wybrana godzina należy do przyszłości."
                            ),
                            html.Li("Wybierz inne miasto, jeśli nie masz wyników."),
                            html.Li(
                                "Dane pogodowe są przybliżone, mogą się różnić od lokalnych."
                            ),
                        ]
                    ),
                ],
                className="ai-suggestion-box",
            ),
        ]
    )
