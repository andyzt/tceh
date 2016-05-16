# -*- coding: utf-8 -*-

"""
This file determines all the settings used in production.
This file is required and if development.py is present
these values are overridden.
"""

from django_orm_example.settings.components.common import (
    BASE_DIR,
    CONFIG,
    TEMPLATES,
)
import os


ADMINS = (
    CONFIG['ADMIN_EMAIL'],
)

MANAGERS = ADMINS


# Installed apps:

# INSTALLED_APPS += (
    # error-handling by sentry and raven:
    # 'raven.contrib.django.raven_compat',
# )


# Production flags:

DEBUG = False

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = False

FRONTEND_DEBUG = False




# Network security and SSL:

ALLOWED_HOSTS = [
    # This setting is required by the 'django-dbbackup' app:
    # 'django-dbbackup'
]


# Static files:

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, 'static'),
)

# This extra directory is used to contain
# both 'static' and 'media' folders.
# The reason is: directory access security settings.
FILES = os.path.join(BASE_DIR, 'files')

# Adding STATIC_ROOT to collect static files via 'collectstatic'
STATIC_ROOT = os.path.join(FILES, 'static_root')

# Media path
MEDIA_ROOT = os.path.join(FILES, 'media')
