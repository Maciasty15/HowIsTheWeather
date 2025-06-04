
#rozwiązanie problemu niewidzących się folderów na tym samym poziomie 
# import os
# import sys
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
# SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'scripts')
# TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')
# sys.path.insert(0, SRC_DIR)
# sys.path.insert(0, SCRIPTS_DIR)
# sys.path.insert(0, TESTS_DIR)


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
