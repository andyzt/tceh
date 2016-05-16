# -*- coding: utf-8 -*-
from datetime import timedelta

import djcelery

djcelery.setup_loader()

# Redis settings:

REDIS_BACKEND = {
    'HOST': 'localhost',
    'PORT': 6379,
    'DB': 0,
}

REDIS_BACKEND_URL = 'redis://{host}:{port}/{db}'.format(
    host=REDIS_BACKEND['HOST'],
    port=REDIS_BACKEND['PORT'],
    db=REDIS_BACKEND['DB'],
)


# CELERY SETTINGS

# If you want to use Redis for storing results (probably not):
# CELERY_RESULT_BACKEND = 'redis://{host}:{port}/{db}'.format(
#     host=REDIS_BACKEND['HOST'],
#     port=REDIS_BACKEND['PORT'],
#     db=REDIS_BACKEND['DB'],
# )

CELERY_RESULT_BACKEND = 'djcelery.backends.database.DatabaseBackend'


CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

BROKER_URL = REDIS_BACKEND_URL

# Periodic tasks:
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"


CELERYBEAT_SCHEDULE = {
    'greet-every-5-seconds': {
        'task': 'pizza.tasks.greet_new_orders',
        'schedule': timedelta(seconds=5),
        # 'args': (16, 16),
    },
}

