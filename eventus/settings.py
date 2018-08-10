import environ

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

INSTALLED_APPS = (
    'cbvadmin',
    'cbvadmin_semantic_ui',
    'semantic_ui',
    'crispy_forms',
    'django_tables2',
    'django_filters',
    'menu',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'comum',
    'eventos',
    'minicursos',
    'trabalhos',
)

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
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
MEDIA_URL = env('MEDIA_URL', default='/media/')
MEDIA_ROOT = env('MEDIA_ROOT', default=str(root.path('uploaded')))
AUTH_USER_MODEL = 'comum.Usuario'

CBVADMIN_SITE_TITLE = env('SITE_TITLE', default='Eventus')
CBVADMIN_TEMPLATE_PACK = 'semantic-ui'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('semantic-ui',)
CRISPY_TEMPLATE_PACK = 'semantic-ui'

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
