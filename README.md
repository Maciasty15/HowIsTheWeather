Aplikacja pobierająca dane pogodowe i o jakości powietrza z publicznych API, 
a następnie sugerująca użytkownikowi odpowiedni ubiór.

Krótka instrukcja uruchamiania:

1. Sklonuj repozytorium
2. zrób uv sync (lub uv init, uv sync)
3. Konfiguruj zmienne środowiskowe: zmień .env.example na .env i uzupełnij klucze

Opis układ folderów:
src/
	core/ - główna logika aplikacji
		__init__.py - technicznie do ulatwienia importow
		weather.py - pobieranie danych o pogodzie (przez skrypty do API w services)
		air_quality.py - pobieranie danych o smogu (przez skrypty do API w services)
		recommender.py - Logika rekomendacji
		settings.py - ładowanie danych do konfiguracji z .env (klucze do API itp)
		
	services/ - Połączenia z api, bazy zewnętrzne
		__init__.py
	
	ui/  - intefejs użytkownika
		__init__.py
	utils/ - narzędzia pomocnicze
		__init__.py
	
tests/

scripts/
	run.py
	main.py - punk wejścia do aplikacji
	
docs/
		
		
		