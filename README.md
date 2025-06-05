Aplikacja pobierająca dane pogodowe i o jakości powietrza z publicznych API, 
a następnie sugerująca użytkownikowi odpowiedni ubiór.

Krótka instrukcja uruchamiania:

1. Sklonuj repozytorium
2. zrób uv sync (lub uv init, uv sync)
3. Konfiguruj zmienne środowiskowe: zmień .env.example na .env i uzupełnij klucze

Opis układ folderów:

main.py - integracja różnych elementów aplikacji
run.py - uruchamianie aplikacji

src/
	core/ - folder głownej logiki aplikacji
		__init__.py - technicznie do ulatwienia importow
		engine.py - główna logika aplikacji
		weather.py - logika pobierania danych o pogodzie (przez skrypty do API w services)
		air_quality.py - logika pobierania danych o smogu (przez skrypty do API w services)
		recommender.py - Logika rekomendacji
		settings.py - ładowanie danych do konfiguracji z .env (klucze do API itp)
		
	services/ - Połączenia z api, bazy zewnętrzne
		__init__.py
	
	ui/  - intefejs użytkownika
		__init__.py
	utils/ - narzędzia pomocnicze
		__init__.py
	
tests/
	__init__.py
	
	
docs/

#####################
Znalezione API
https://www.weatherapi.com/

		
###########################
Użycie logów:
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    datefmt="%d.%m.%Y %H:%M")
#logging.disable(logging.CRITICAL)  # ← Wyłącza wszystkie logi
#logger.debug("Tekst") # <- przykład użycia


########################## Rozwiązania znanych problemów #########
#w razie konieczności do testów: rozwiązanie problemu niewidzących się folderów na tym samym poziomie 
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'scripts')
TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, TESTS_DIR)
		