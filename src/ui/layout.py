from dash import html, dcc
import datetime
from src.core.constants import city_ids, city_names


def create_layout():
    now = datetime.datetime.now()

    return html.Div(
        [
            dcc.Store(id="store-weather", data={}),
            dcc.Store(id="store-air", data={}),
            dcc.Store(id="store-gemini", data=""),
            dcc.Store(id="store-city", data=""),
            dcc.Store(id="store-datetime", data=""),
            html.H1("HowIsTheWeather", className="title"),
            html.P(
                """
    Nasza aplikacja pozwoli ci:
    - sprawdzić aktualną pogodę
    - sprawdzić aktualne zanieczyszczenie powietrza
    - doradzić Ci w kwestii aktywności fizycznej
    - doradzić Ci w kwestii doboru odpowiedniej odzieży
    """,
                className="intro-text",
            ),
            html.H2("Wybierz miasto", className="section-title"),
            html.Div(
                [
                    html.Button(city, id=btn_id, className="city-button")
                    for city, btn_id in zip(city_names, city_ids)
                ],
                className="city-button-container",
            ),
            html.Div(
                id="selected-city", style={"marginTop": "10px", "textAlign": "center"}
            ),
            html.Div(
                [
                    html.P("Wybierz datę i godzinę", className="section-title"),
                    dcc.DatePickerSingle(
                        id="date-picker",
                        date=now.today(),
                        display_format="YYYY-MM-DD",
                        className="date-picker",
                    ),
                    html.Div(
                        [
                            dcc.Input(
                                id="hour-input",
                                type="number",
                                placeholder="HH",
                                min=0,
                                max=23,
                                value=now.hour,
                                className="time-input",
                            ),
                            dcc.Input(
                                id="minute-input",
                                type="number",
                                placeholder="MM",
                                min=0,
                                max=59,
                                value=now.minute,
                                className="time-input",
                            ),
                            html.Button(
                                "Zatwierdź datę i czas",
                                id="confirm-time",
                                className="confirm-button",
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
            html.H2("Twoja Prognoza Pogody", className="section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("Temperatura", className="label"),
                            html.Span(id="temp-c", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Wiatr", className="label"),
                            html.Span(id="wind-kph", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Zachmurzenie", className="label"),
                            html.Span(id="cloud", children="--", className="value"),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Span("Szansa na deszcz", className="label"),
                            html.Span(id="rain", children="--", className="value"),
                        ],
                        className="row",
                    ),
                ],
                className="forecast-box",
            ),
            html.H2("Jakość powietrza na dzień prognozy", className="section-title"),
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
                ],
                className="air-quality-box",
            ),
            html.H2(
                "Zalecenia asystenta AI co do ubioru i aktywności",
                className="section-title",
            ),
            dcc.Markdown(id="ai-suggestion-box", className="ai-suggestion-box"),
        ]
    )
