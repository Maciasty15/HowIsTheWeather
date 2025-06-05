from src.utils.logger import get_logger

logger = get_logger(__name__)

class App:
    """
    Klasa reprezentuje punkt wejścia do aplikacji.
    Zdecydowano się rozdzielić ją z core/main dla ułatwienia późniejszego testowania osobno logiki a osobno uruchamiania aplikacji
    """

    def __init__(self):
        logger.debug("Inicjalizuję aplikacje")

    def run(self):
        logger.debug("Uruchamiam logikę aplikacji")
        #TODO Tu będzie uruchamianie logiki aplikacji poprzez integracje z src/core/engine.py



# To co było wcześniej w tym pliku, raczej będzie przeniesione do UI?
# import dash
# from dash import html

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.P("Hello world")
#     ])

# if __name__ == "__main__":
#     app.run(debug=True)
