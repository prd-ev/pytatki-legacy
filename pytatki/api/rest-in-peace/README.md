# Pytatki - API

Instrukcja API aplikacji

## User
Akcje z użytkownikiem
### Info o użytkowniku
Wymgane uprawnienia administratora
```
$ curl -X GET -u twoj_login:twoje_haslo http://pytatki-beta.pl/api/user/nazwa_uzytkownika/
{
  "access": {
    "admin": false, 
    "ban": false, 
    "mod": false, 
    "superuser": false
  }, 
  "confirm_email": true, 
  "email": "email@uzytkownika", 
  "username": "nazwa_uzytkownika"
}
```
### Lista użytkowników
Wymagane uprawnienia administratora
```
$ curl -X GET -u twoj_login:twoje_haslo http://pytatki-beta.pl/api/user/
{
  "1": {
    "access": {
      "admin": false, 
      "ban": false, 
      "mod": false, 
      "superuser": false
    }, 
    "confirm_email": true, 
    "email": "email@uzytkownika", 
    "username": "nazwa_uzytkownika"
  "2": {
  ...
}
```
### Dodawanie użytkownika
```
$ curl -H "Content-Type: application/json" -X POST -d '{"username":"login","password":"haslo","email":"twoj@email"}' http://localhost:5000/api/user/
{
  "access": {
    "admin": false, 
    "ban": false, 
    "mod": false, 
    "superuser": false
  }, 
  "confirm_email": false, 
  "email": "twoj@email", 
  "username": "login"
}
```
### Usuwanie użytkownika
```
$ curl -X DELETE -u twoj_login:haslo http://localhost:5000/api/user/login/
{
  "data": "User login deleted"
}
```
Dla użytkownika który nie istnieje zwraca
```
$ curl -X DELETE -u twoj_login:haslo http://localhost:5000/api/user/fdfbrgrbrbnt/
{
  "data": "User doesn't exist"
}
```
##### Note: W przypadku niepoprawnych danych lub próby usunięcia su zwróci:
```
{
  "data": "Permission denied"
}
```
