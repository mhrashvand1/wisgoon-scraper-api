from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="fbytght54e9uhgoc")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=lambda value: bool(int(value)))

def parse_list_cast(value):
    if type(value) == str:
        return [i.strip() for i in value.split()]
    elif type(value) in [list, tuple]:
        return [i.strip() for i in value]
    else:
        return value
    
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=parse_list_cast,
    default=["*"]
)

INTERNAL_IPS = config(
    "INTERNAL_IPS",
    cast=parse_list_cast,
    default=["*"]
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party packages
    "django_filters",
    "rest_framework",
    # project apps
    'account.apps.AccountConfig',
    'core.apps.CoreConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="wisgoon_scraper"),
        "USER": config("DB_USER", default="wisgoon_scraper"),
        "PASSWORD": config("DB_PASSWORD", default="wisgoon_scraper"),
        "HOST": config("DB_HOST", default="postgres"),
        "PORT": config("DB_PORT", default=5432),
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent.parent / 'static'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent.parent / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# User Model
AUTH_USER_MODEL = 'account.User'

# drf
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        # session authentication
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS':(
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ),
    'DEFAULT_PAGINATION_CLASS':'common.paginations.StandardPagination'
}


# URL
PROJECT_HOST = "127.0.0.1"
if DEBUG:
    PROJECT_PORT = "8000"
else:
    PROJECT_PORT = "80"  
PROJECT_SCHEMA = "http" 


# Rabbitmq:
# RABBITMQ_USER = config('RABBITMQ_USER', default="wisgoon_scraper")
# RABBITMQ_PASS = config('RABBITMQ_PASS', default="wisgoon_scraper")
# RABBITMQ_VHOST = config('RABBITMQ_VHOST', default="wisgoon_scraper")
# RABBITMQ_HOST = config('RABBITMQ_HOST', default="rabbitmq")
# RABBITMQ_PORT = config('RABBITMQ_PORT', default=5672)

# redis
REDIS_HOST = config("REDIS_HOST", "redis")
REDIS_PORT = config("REDIS_PORT", 6379)

# Celery settings:
# CELERY_BROKER_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
# CELERY_RESULT_EXPIRES = 3000
CELERY_TASK_ROUTES = {
    'core.tasks.run_crawler_task':{'queue':'run_crawler_queue'},
}

