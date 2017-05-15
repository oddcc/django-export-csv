import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'HARD_TO_GUESS'

DEBUG = True

INSTALLED_APPS = (
    'export_csv',
)

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'export_csv.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
