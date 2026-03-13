import pytest

@pytest.fixture(autouse=True)
def _test_settings_overrides(settings):
    """
    Overrides settings for the test environment.
    """
    settings.CASBIN_ADAPTER = "memory"
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_BROKER_URL = "memory://"
    settings.CELERY_RESULT_BACKEND = "cache"
    settings.CELERY_CACHE_BACKEND = "memory"

