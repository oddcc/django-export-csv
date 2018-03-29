from __future__ import unicode_literals
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '+^jd4@x8l1353bu8)_*p_ii0l7q32+-6je!4*r7sx56y-&=!_8'

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',

    'tests.core',
    'export_csv',
]

ROOT_URLCONF = 'tests.core.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}