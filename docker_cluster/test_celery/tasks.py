from __future__ import absolute_import
from celery_test import make_celery
import schedule
import time
from flask import Flask

flask = Flask(__name__)
flask.config['CELERY_RESULT_BACKEND'] = 'rpc://'
flask.config['CELERY_BROKER_URL'] = 'amqp://localhost'

app = make_celery(flask)

def job():
    print("xd")

schedule.every().second.do(job)

@app.task(name='tasks.run_jobs')
def run_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_jobs.delay()
    flask.run()
