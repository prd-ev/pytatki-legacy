from __future__ import absolute_import
from test_celery.celery import app
import schedule
import time

def job():
    print("xd")

schedule.every().second.do(job)

@app.task
def run_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)
