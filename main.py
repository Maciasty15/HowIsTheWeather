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
        # TODO Tu będzie uruchamianie logiki aplikacji poprzez integracje z src/core/engine.py


#DEBUG!!!:
from src.ui import index

app.run()