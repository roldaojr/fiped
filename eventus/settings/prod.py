from .comum import *

DEBUG = False
ALLOWED_HOSTS = ['0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('EVENTUS_DB_NAME', 'eventus'),
        'USER': os.environ.get['EVENTUS_DB_USERNAME', 'eventus'),
        'PASSWORD': os.environ.get('EVENTUS_DB_PASSWORD', ''),
        'HOST': os.environ.get('EVENTUS_DB_HOST', 'localhost'),
        'PORT': os.environ.get('EVENTUS_DB_PORT', 3306)
    }
}
