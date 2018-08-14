import sys
import environ
from cbvadmin_semantic_ui.settings import update_cbvadmin_settings

TESTIMG = len(sys.argv) > 1 and sys.argv[1] == 'test'

update_cbvadmin_settings(locals())

env_settings = {
    'DEBUG': (bool, True),
    'SECRET_KEY': (str, 'dummy'),
    'ALLOWED_HOSTS': (list, ['*']),
}

root = environ.Path(__file__) - 2
env = environ.Env(**env_settings)

BASE_DIR = root()
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'comum',
    'eventos',
    'trabalhos',
    'cbvadmin',
    'cbvadmin_semantic_ui',
    'semantic_ui',
    'crispy_forms',
    'django_tables2',
    'django_filters',
    'menu',
    'registration',
    'dynamic_preferences',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eventus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dynamic_preferences.processors.global_preferences',
            ],
        },
    },
]

WSGI_APPLICATION = 'eventus.wsgi.application'

DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3')
}

EMAIL_CONFIG = env.email_url('EMAIL_URL', default='consolemail://')
vars().update(EMAIL_CONFIG)

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Fortaleza'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = env('STATIC_URL', default='/static/')
STATIC_ROOT = env('STATIC_ROOT', default=str(root.path('static')))

if not TESTIMG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = env('MEDIA_URL', default='/media/')
MEDIA_ROOT = env('MEDIA_ROOT', default=str(root.path('media')))
AUTH_USER_MODEL = 'comum.Usuario'

CBVADMIN_TEMPLATE_PACK = 'semantic-ui'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('semantic-ui',)
CRISPY_TEMPLATE_PACK = 'semantic-ui'

# Regstration
ACCOUNT_ACTIVATION_DAYS = 2
REGISTRATION_DEFAULT_FROM_EMAIL = None
REGISTRATION_EMAIL_HTML = True
REGISTRATION_FORM = 'eventos.forms.InscricaoForm'
INCLUDE_AUTH_URLS = False

# Configure debug toolbar
DEBUG_TOOLBAR = env('DEBUG_TOOLBAR', default=DEBUG)
try:
    import debug_toolbar
except ImportError:
    DEBUG_TOOLBAR = False

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_COLLAPSED': True
    }
