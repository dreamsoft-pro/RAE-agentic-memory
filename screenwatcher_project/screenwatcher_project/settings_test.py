from .settings import *
import os

# Disable SSL redirect in test settings
SECURE_SSL_REDIRECT = False

# Run Celery tasks synchronously for testing
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache'
CELERY_CACHE_BACKEND = 'memory'

# Use in-memory channel layer for testing
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Disable Casbin for tests to simplify API testing
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.IsAuthenticated',
]

# Static files for testing (WhiteNoise)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_test')
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT, exist_ok=True)