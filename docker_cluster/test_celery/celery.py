from __future__ import absolute_import
from celery import Celery
app = Celery('test_celery', broker='amqp://pytatki:pytatki@127.0.0.1:5673',
             backend='rpc://', include=['test_celery.tasks'])
