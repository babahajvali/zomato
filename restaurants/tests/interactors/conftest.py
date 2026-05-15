import pytest
from django.core.cache import cache

from utils import caching_decorators


class _DummyCache:
    def get(self, key):
        return None

    def set(self, key, value, timeout=None):
        return None

    def delete_pattern(self, pattern):
        return None


@pytest.fixture(autouse=True)
def patch_interactor_cache(monkeypatch):
    dummy_cache = _DummyCache()
    monkeypatch.setattr(caching_decorators, "cache", dummy_cache)
    monkeypatch.setattr(cache, "clear", lambda: None)
