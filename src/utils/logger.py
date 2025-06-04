import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    datefmt="%d.%m.%Y %H:%M")

def get_logger(name: str):
    return logging.getLogger(name)

#logging.disable(logging.CRITICAL)  # ← Wyłącza wszystkie logi
#logger.debug("Tekst") # <- przykład użycia
#logger.setLevel(logging.CRITICAL + 1)  # Wycisza ten konkretny logger
#logger.setLevel(logging.DEBUG)