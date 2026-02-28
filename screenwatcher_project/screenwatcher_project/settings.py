"""
Django settings for the ScreenWatcher project.
"""
from __future__ import annotations
import os
from pathlib import Path
from django.templatetags.static import static
import environ
import pymysql
pymysql.install_as_MySQLdb()

env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    'daphne',
    'corsheaders',  # ASGI Support (Channels)

    'unfold',
    'unfold.contrib.filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',  # Token Authentication
    'drf_spectacular',
    'django_celery_results',
    'channels',
    'casbin_adapter',

    # ScreenWatcher Apps
    'apps.core',
    'apps.accounts',
    'apps.rbac',
    'apps.registry',
    'apps.collector',
    'apps.telemetry',
    'apps.oee',
    'apps.rules',
    'apps.dashboards',
    'apps.notifications',
    'apps.operator_panel',
    'apps.reports',
    'apps.api',
    'apps.legacy_integration',
    'apps.mcp_server',
    'apps.audit',

    # Legacy (Disabled)
    # 'apps.configurator',
    # 'apps.data_ingestion',
    # 'apps.data_forwarding',
    # 'apps.statistics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'apps.audit.middleware.AuditMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Security settings
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
SECURE_BROWSER_XSS_FILTER = env.bool('SECURE_BROWSER_XSS_FILTER', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000) # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=True)

ROOT_URLCONF = 'screenwatcher_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'screenwatcher_project.wsgi.application'
ASGI_APPLICATION = 'screenwatcher_project.asgi.application'

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

if os.getenv('USE_MYSQL', 'false').lower() == 'true':
    DATABASES: Dict[str, Dict[str, Any]] = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'screenwatcher'),
            'USER': os.getenv('DB_USER', 'screenwatcher'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1;",
            },
        },
        'external_legacy': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('EXTERNAL_DB_NAME', 'tjdata'),
            'USER': os.getenv('EXTERNAL_DB_USER', 'TruJetBarcoding'),
            'PASSWORD': os.getenv('EXTERNAL_DB_PASSWORD', ''),
            'HOST': os.getenv('EXTERNAL_DB_HOST', 'tjreader.printdisplay.pl'),
            'PORT': os.getenv('EXTERNAL_DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    DATABASES: Dict[str, Dict[str, Any]] = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'external_legacy': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db_legacy.sqlite3',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Channel layer settings
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': { "hosts": [env.str('REDIS_URL', 'redis://localhost:6379/1')] },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework configuration
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'apps.core.exception_handler.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'apps.rbac.permissions.CasbinPermission',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'ScreenWatcher Professional API',
    'DESCRIPTION': '''
# ScreenWatcher Operational Intelligence API

Comprehensive industrial monitoring system providing:
* **Real-time OEE** (Availability, Performance, Quality)
* **Telemetry Ingestion** for Edge devices
* **RBAC** (Casbin-based) granular security
* **Audit Logging** (ISO 27001 compliant)
* **Rules Engine** for automated reasoning

For authentication, use: `Authorization: Token <your_token>`
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'ScreenWatcher Support',
        'url': 'https://screenwatcher.pro',
        'email': 'support@screenwatcher.pro'
    },
    'LICENSE': {
        'name': 'Proprietary',
    },
    'TAGS': [
        {'name': 'Registry', 'description': 'Asset management (Factories, Lines, Machines)'},
        {'name': 'Collector', 'description': 'Telemetry and data ingestion'},
        {'name': 'OEE', 'description': 'Performance metrics and calculations'},
        {'name': 'Rules', 'description': 'Business logic and automated alerts'},
        {'name': 'Audit', 'description': 'Compliance and security logs'},
    ],
}

# Celery configuration
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', 'django-db')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

# Casbin Configuration
CASBIN_MODEL = os.path.join(BASE_DIR, 'apps/rbac/config/rbac_model.conf')

# Database Routers
DATABASE_ROUTERS = ['apps.legacy_integration.router.LegacyDatabaseRouter']

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False)
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:3000'])
CORS_ALLOW_CREDENTIALS = True

# Security Settings (Overrides)
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

# Unfold Admin Theme Configuration
UNFOLD = {
    "SITE_TITLE": "ScreenWatcher Admin",
    "SITE_HEADER": "ScreenWatcher Administration",
    "SITE_URL": "/",
    # "SITE_ICON": "img/logo.png",  # TODO: Add logo
    "STYLES": [
        lambda request: static("css/admin_patch.css"),
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Navigation",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": "/dashboard/",
                    },
                    {
                        "title": "API Docs",
                        "icon": "description",
                        "link": "/api/schema/swagger-ui/",
                        "permission": lambda request: request.user.is_authenticated,
                    },
                ],
            },
        ],
    },
    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
            "950": "23 37 84",
        },
    },
}
