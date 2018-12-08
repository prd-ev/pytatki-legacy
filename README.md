# No longer in development!

# pytatki

[![CodeFactor](https://www.codefactor.io/repository/github/PRD-ev/pytatki/badge)](https://www.codefactor.io/repository/github/PRD-ev/pytatki)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/888414de92604fbbbd46b42c04e96e81)](https://www.codacy.com/app/pniedzwiedzinski19/pytatki?utm_source=github.com&utm_medium=referral&utm_content=butterfly-pn/pytatki&utm_campaign=Badge_Grade)
[![CircleCI](https://circleci.com/gh/PRD-ev/pytatki/tree/master.svg?style=svg)](https://circleci.com/gh/PRD-ev/pytatki/tree/master)
[![Issues](https://img.shields.io/github/issues/PRD-ev/pytatki.svg)](https://github.com/PRD-ev/pytatki/issues)
![Snakes](https://img.shields.io/badge/version-v1.1.2-blue.svg)

Pytatki is an open source web app for storing notes and learning resources. The purpose of this app is to make organizing them easier and faster.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Instalation

Clone this repo

```
git clone https://github.com/PRD-ev/pytatki.git
```

Install Flask dependencies

```
pip install -r requirements/common.txt
```

Install React dependencies

```
yarn add
```

Build bundles

```
yarn run build
```

### Configuration

Create `config.json` file in root directory of repository. You can find an example in `examples` folder.

```json
{
  "default": {
    "secret_key": "change_it",
    "debug": true,
    "host": "127.0.0.1",
    "port": 5000
  },
  "email": {
    "mail_server": "smtp.gmail.com",
    "mail_port": 587,
    "mail_use_ssl": false,
    "mail_use_tls": true,
    "email": "your_mail@gmail.com",
    "email_password": "your_password"
  },
  "database": {
    "db_host": "127.0.0.1",
    "db_user": "pytatki",
    "db_password": "pytatki",
    "db_name": "pytatki"
  }
}
```

To configure database run `init_db.py` script.

## Testing

###

```
pytest
jest
```

## Built With

- [Bootstrap](https://www.getbootstrap.com/)
- [Flask](http://flask.pocoo.org/)
- [React](https://reactjs.org)

## Contributing 🎉

Feel free to contribute 😜. If you want to contact owners: [CONTRIBUTING.md](https://github.com/butterfly-pn/pytatki/blob/master/docs/CONTRIBUTING.md)

## Authors

- **Patryk Niedźwiedziński** - _Initial work_ - [butterfly-pn](https://github.com/butterfly-pn)
- **Filip Wachowiak** - _React developer_ - [filipw01](https://github.com/filipw01)

Check out [contributors](https://github.com/butterfly-pn/pytatki/graphs/contributors)

## TODO

- [ ] Add new note (tags, notegroup etc.)
- [x] Login, register + admin
- [ ] Search
- [ ] Manage note (delete, hide, properties etc.)
- [x] Usergroups
