# -*- coding: utf-8 -*-

"""
This file determines all the settings that must define the testing server.
Basically it copies the development settings. It is included in VCS.

SECURITY WARNING: don't run with debug turned on in production!
"""

# Mind the proper import, use the right module!
from django_orm_example.settings.components.common import (
    INSTALLED_APPS,
    MIDDLEWARE_CLASSES,
    TEMPLATES,
    BASE_DIR,
    CONFIG,
    DATABASES,
)

import os

# Setting the development status:

DEBUG = True

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

FRONTEND_DEBUG = True

ALLOWED_HOSTS = []

# DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'


# Template Debug settings:
# http://django-debug-toolbar.readthedocs.org/en/latest/index.html

INSTALLED_APPS += (
    'debug_toolbar',

    'django_behave',
    # 'template_timings_panel',
)

# Testing:

# Use nose to run all tests
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'

# Tell nose to measure coverage on the apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=main_app',
    '--cover-html',
]

DEBUG_TOOLBAR_PATCH_SETTINGS = False

MIDDLEWARE_CLASSES += (
    'querycount.middleware.QueryCountMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PANELS = [
    # django-debug-toolbar:
    'debug_toolbar.panels.sql.SQLPanel',

    # django-debug-toolbar-template-timings:
    # https://github.com/orf/django-debug-toolbar-template-timings
    # 'template_timings_panel.panels.TemplateTimings.TemplateTimings',

    # django-debug-toolbar:
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

# Django-QueryCount:
QUERYCOUNT = {
    'IGNORE_REQUEST_PATTERNS': [
        r'^/admin/',
        r'^__debug__/',
    ]
}

# Network security and SSL:

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    # '0.0.0.0',

    # Uncomment next line and run
    # 'runserver 0.0.0.0:8000' for production test:
    # '192.168.(insert).(yours)'
]


# Static files:
# https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-STATICFILES_DIRS

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, 'bitcoins', 'static'),

    # Adding frontend package managers in development:
    # os.path.join(BASE_DIR, 'node_modules'),
    os.path.join(BASE_DIR, 'bower_components'),
)

# Adding STATIC_ROOT to collect static files via 'collectstatic'.
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

# Media files root:

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s "
                      "[%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'server.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'server': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
