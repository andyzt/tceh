# -*- coding: utf-8 -*-

"""
To run celery:
`celery --app=django_orm_example.celery_app:app worker --loglevel=INFO -E -B`
`python manage.py celerycam`
"""

import os

from celery import Celery
from django.conf import settings

__author__ = 'sobolevn'

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'django_orm_example.settings')

app = Celery('pizza')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
