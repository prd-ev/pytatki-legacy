#!./venv/bin python3
from pytatki.user import *
from pytatki.views import *
from pytatki.main import APP, CONFIG
from pytatki.tasks.tasks import run_jobs, remove_bin


if __name__ == '__main__':
    run_jobs.delay()
    APP.run(debug=CONFIG['default']['debug'], host=CONFIG['default']
            ['host'], port=CONFIG['default']['port'])
