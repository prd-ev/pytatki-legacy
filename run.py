#!./venv/bin python3
from pytatki.user import *
from pytatki.views import *
from pytatki.main import APP, CONFIG


if __name__ == '__main__':
    APP.run(debug=CONFIG['DEFAULT']['DEBUG'], host=CONFIG['DEFAULT']['HOST'], port=CONFIG['DEFAULT']['PORT'])
