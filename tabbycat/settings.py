import os

from django.contrib.messages import constants as messages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==============================================================================
# Overwritten in Local
# ==============================================================================

ADMINS = ('Philip and Chuan-Zheng', 'tabbycat@philipbelesky.com'),
MANAGERS = ADMINS
DEBUG = bool(int(os.environ['DEBUG'])) if 'DEBUG' in os.environ else False
DEBUG_ASSETS = DEBUG

# ==============================================================================
# Global Settings
# ==============================================================================

MEDIA_URL = '/media/'
TIME_ZONE = 'Australia/Melbourne'
LANGUAGE_CODE = 'es'
USE_I18N = True

TABBYCAT_VERSION = '2.0.5'
TABBYCAT_CODENAME = 'Iberian Lynx'
READTHEDOCS_VERSION = 'v2.0.5'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# ==============================================================================
# Django-specific Module
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For Static Files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware.DebateMiddleware'
]

TABBYCAT_APPS = ('actionlog',
                 'adjallocation',
                 'adjfeedback',
                 'availability',
                 'breakqual',
                 'divisions',
                 'draw',
                 'motions',
                 'options',
                 'participants',
                 'printing',
                 'privateurls',
                 'results',
                 'tournaments',
                 'venues',
                 'utils',
                 'users',
                 'standings',
                 'importer', )

INSTALLED_APPS = (
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'whitenoise.runserver_nostatic',  # Use whitenoise with runserver
    'raven.contrib.django.raven_compat',  # Client for Sentry error tracking
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.messages') \
    + TABBYCAT_APPS + (
    'dynamic_preferences',
    'dynamic_preferences.users.apps.UserPreferencesConfig',
    'django_extensions',  # For Secret Generation Command
    'gfklookupwidget',
    'formtools')

ROOT_URLCONF = 'urls'
LOGIN_REDIRECT_URL = '/'

# ==============================================================================
# Templates
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',  # for Jet
                'utils.context_processors.debate_context',  # for tournament config vars
                'utils.context_processors.get_menu_highlight',  # for navigation highlights
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ]
        }
    }
]

# ==============================================================================
# Caching
# ==============================================================================

PUBLIC_PAGE_CACHE_TIMEOUT = int(os.environ.get('PUBLIC_PAGE_CACHE_TIMEOUT', 60 * 1))
TAB_PAGES_CACHE_TIMEOUT = int(os.environ.get('TAB_PAGES_CACHE_TIMEOUT', 60 * 120))

# Default non-heroku cache is to use local memory
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

# Use a db backed cache for sessions unless the app is retired (no db writes)
if 'RETIRED' in os.environ:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
else:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# ==============================================================================
# Static Files and Compilation
# ==============================================================================

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Whitenoise Gzipping and unique names
STATICFILES_STORAGE = 'utils.misc.SquashedWhitenoiseStorage'

# ==============================================================================
# Logging
# ==============================================================================

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

if os.environ.get('SENDGRID_USERNAME', ''):
    SERVER_EMAIL = os.environ['SENDGRID_USERNAME']
    DEFAULT_FROM_EMAIL = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'except_importer_base': {
            '()': 'utils.logging.ExceptFilter',
            'name': 'importer.importers.base',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'filters': ['except_importer_base'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'django.request': {
            'handlers': ['sentry'],
            'level': 'ERROR',
        },
        'raven': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s',
        },
    },
}

for app in TABBYCAT_APPS:
    LOGGING['loggers'][app] = {
        'handlers': ['console', 'sentry'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    }

# ==============================================================================
# Sentry
# ==============================================================================

DISABLE_SENTRY = True

if 'DATABASE_URL' in os.environ and not DEBUG:
    DISABLE_SENTRY = False  # Only log JS errors in production on heroku

    RAVEN_CONFIG = {
        'dsn': 'https://6bf2099f349542f4b9baf73ca9789597:57b33798cc2a4d44be67456f2b154067@sentry.io/185382',
        'release': TABBYCAT_VERSION,
    }

    # Custom implementation makes the user ID the e-mail address, rather than the primary key
    SENTRY_CLIENT = 'utils.raven.TabbycatRavenClient'

# ==============================================================================
# Messages
# ==============================================================================

MESSAGE_TAGS = {messages.ERROR: 'danger', }

# ==============================================================================
# Heroku
# ==============================================================================

# Get key from heroku config env else use a fall back
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', r'#2q43u&tp4((4&m3i8v%w-6z6pp7m(v0-6@w@i!j5n)n15epwc')

# Parse database configuration from $DATABASE_URL
try:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default='postgres://localhost')
    }
except:
    pass

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Require HTTPS
if 'DJANGO_SECRET_KEY' in os.environ and os.environ.get('DISABLE_HTTPS_REDIRECTS', '') != 'disable':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Store Tab Director Emails for reporting purposes
if 'TAB_DIRECTOR_EMAIL' in os.environ:
    TAB_DIRECTOR_EMAIL = os.environ.get('TAB_DIRECTOR_EMAIL', '')

# Memcache Services
if os.environ.get('MEMCACHIER_SERVERS', ''):
    try:
        os.environ['MEMCACHE_SERVERS'] = os.environ[
            'MEMCACHIER_SERVERS'].replace(',', ';')
        os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
        os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
        CACHES = {
            'default': {
                'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
                'TIMEOUT': 36000,
                'BINARY': True,
                'OPTIONS': {  # Maps to pylibmc "behaviors"
                    # Enable faster IO
                    'no_block': True,
                    'tcp_nodelay': True,
                },
                # Timeout for set/get requests
                '_poll_timeout': 2000,
            }
        }
    except:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
            }
        }

# ==============================================================================
# Travis CI
# ==============================================================================

FIXTURE_DIRS = (os.path.join(os.path.dirname(BASE_DIR), 'data', 'fixtures'), )

if os.environ.get('TRAVIS', '') == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

# ==============================================================================
# Local Overrides and Docker
# ==============================================================================

# Hide league-related configuration options unless explicitly enabled
LEAGUE = bool(int(os.environ['LEAGUE'])) if 'LEAGUE' in os.environ else False

# Must default to false; potentially overridden in local_settings
ENABLE_DEBUG_TOOLBAR = False

if os.environ.get('IN_DOCKER', '') and bool(int(os.environ['IN_DOCKER'])):
    DEBUG = True # Just to be sure
    ALLOWED_HOSTS = ["*"]
    DATABASES = {
        'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'tabbycat',
             'USER': 'tabbycat',
             'PASSWORD': 'tabbycat',
             'HOST': 'db',
             'PORT': 5432, # Non-standard to prevent collisions
        }
    }
else:
    try:
        LOCAL_SETTINGS
    except NameError:
        try:
            from local_settings import *   # noqa
        except ImportError:
            pass
