# pytatki
[![CodeFactor](https://www.codefactor.io/repository/github/PRD-ev/pytatki/badge)](https://www.codefactor.io/repository/github/PRD-ev/pytatki)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/888414de92604fbbbd46b42c04e96e81)](https://www.codacy.com/app/pniedzwiedzinski19/pytatki?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=butterfly-pn/pytatki&amp;utm_campaign=Badge_Grade)
[![CircleCI](https://circleci.com/gh/PRD-ev/pytatki/tree/master.svg?style=svg)](https://circleci.com/gh/PRD-ev/pytatki/tree/master)

Notatki we flasku

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Instalation

Clone this repo
```
git clone https://github.com/PRD-ev/pytatki.git
```
Install dependencies
```
pip install -r requirements/common.txt
```
### Configuration
Create `config.ini` file in root directory of repository. You can find an example in `examples` folder.


```
[DEFAULT]
secret_key = "your_own_secret_key" # Don't leave default value
DEBUG = True
HOST = 127.0.0.1
PORT = 5000

[DATABASE]
DB_HOST = '127.0.0.1'
DB_USER = 'pytatki'
DB_PASSWORD = 'pytatki'
DB_NAME = 'pytatki'
```

To configure database run `init_db.py` script.

## Testing
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

- [ ] Dodawanie plików/notatek (dodanie tagów, przedmiotu itd.)
- [x] Logowanie i rejestracja + admin
- [ ] Wyszukiwanie notatek
- [ ] Zarządzanie notatkami (usuń, ukryj itp.)
- [x] Podział użytkowników na grupy
