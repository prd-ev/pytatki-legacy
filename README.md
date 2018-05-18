# pytatki
[![CodeFactor](https://www.codefactor.io/repository/github/butterfly-pn/pytatki/badge)](https://www.codefactor.io/repository/github/butterfly-pn/pytatki)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/888414de92604fbbbd46b42c04e96e81)](https://www.codacy.com/app/pniedzwiedzinski19/pytatki?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=butterfly-pn/pytatki&amp;utm_campaign=Badge_Grade)
[![CircleCI](https://circleci.com/gh/butterfly-pn/pytatki.svg?style=svg)](https://circleci.com/gh/butterfly-pn/pytatki)

Notatki we flasku

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Wymagania

Aby uruchomić aplikację potrzebne są odpowiednie moduły python'a. Można je pobrać za pomocą pip'a wpisując następujące komendy:

```
pip install flask
pip install sqlalchemy
pip install passlib
pip install requests
pip install bcrypt
pip install uwsgi
```

### Instalacja

Sklonuj to repozytorium na komputer, na którym chcesz uruchomić aplikację
```
git clone https://github.com/butterfly-pn/pytatki.git
```
Następnie otwórz plik config/\_\_init\_\_.py. Pytatki pozwalają zapisać dwa presety ustawień `Localhost` i `Server`. Dzięki temu możesz testować aplikację lokalnie, a gdy wszystko będzie gotowe wystarczy zmienić tylko jedną linijką, żeby udostępnić światu aplikację :).


```
class Localhost:
    '''Do testowania na komputerze lokalnym'''
    secret_key = str()
    DEBUG = True #True oznacza, że aplikacja będzie sprawdzać zmiany w plikach
    HOST = "127.0.0.1" #Tutaj wpisujemy adres, na którym chcemy postawić stronę
    PORT = 5000 #Tutaj wpisujemy port, na którym ma działać aplikacja
    EMAIL = "twoj@email" #Z tego maila wysyłane będą powiadomienia do użytkowników
    EMAIL_PASSWORD = "haslo_do_twojego_maila" #Hasło do maila
    
    (...)
    
CONFIG = Localhost("sekretny_klucz") #W nawiasie wpisujemy klucz do szyfrowania haseł w bazie danych
# NIE ZATRZYMUJ WARTOŚCI DOMYŚLNEJ!
```

Żeby uruchomić aplikację wpisz:

```
python main.py
```


## Testowanie
### 
```
pytest
```

## Built With

* [Bootstrap](https://www.getbootstrap.com/) 
* [Flask](http://flask.pocoo.org/) 

## Współpraca

Jesteśmy na każdą formę współpracy :). Dane kontaktowe można znaleźć w pliku [CONTRIBUTING.md](https://github.com/butterfly-pn/pytatki/blob/master/docs/CONTRIBUTING.md)


## Autorzy

* **Patryk Niedźwiedziński** - *Initial work* - [butterfly-pn](https://github.com/butterfly-pn)
* **Filip Wachowiak** - [filipw01](https://github.com/filipw01)

Zobacz również listę [współautorów](https://github.com/butterfly-pn/pytatki/graphs/contributors), którzy przyczynili się w rozwoju aplikacji.




## TODO

1. Dodawanie plików/notatek (dodanie tagów, przedmiotu itd.)
2. Logowanie i rejestracja + admin
3. Wyszukiwanie notatek
4. Zarządzanie notatkami (usuń, ukryj itp.)
5. Podział użytkowników na klasy
