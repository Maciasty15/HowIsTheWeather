Aplikacja „HowIsTheWeather” pokazuje aktualną pogodę i jakość powietrza w wybranym mieście. Podpowiada też, jak się ubrać w zależności od warunków na zewnątrz. Wszystko działa automatycznie i jest łatwe w obsłudze.


Krótka instrukcja uruchamiania:

1. Sklonuj repozytorium
2. skonfiguruj otrzymane klucze w pliku .env

  
3A)Aby po prostu uruchomić aplikację uruchom skrypt run.py
działanie aplikacji zobaczysz pod adresem
http://127.0.0.1:8050/

Alternatywnie:
3B) Możesz też uruchomić aplikację w kontenerze dockera:
Uruchom docker desktop
wpisz w terminalu w VSC
docker compose up --build
 
działanie aplikacji zobaczysz pod adresem
http://127.0.0.1:8050/
 
po zakończeniu aplikacji wprowadź
 
docker compose down     
 
aby zakończyć jej działanie

