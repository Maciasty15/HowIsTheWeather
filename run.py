
"""
Run repezentuje skrypt do uruchamiania calej aplikacji jednym kliknięciem"""

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    datefmt="%d.%m.%Y %H:%M")
#logging.disable(logging.CRITICAL)  # ← Wyłącza wszystkie logi
#logger.debug("Tekst") # <- przykład użycia

from main import App

if __name__ == "__main__":
    app = App()
    app.run()