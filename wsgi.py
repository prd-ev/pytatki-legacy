from src.views import *
from src.user import *
from main import APP
import time

@APP.route('/long/')
def long_test():
    time.sleep(5)
    return "x"

if __name__ == '__main__':
    APP.run(debug=CONFIG.DEBUG, host=CONFIG.HOST, port=CONFIG.PORT)
