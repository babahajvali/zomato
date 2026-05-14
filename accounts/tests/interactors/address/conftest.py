import pytest

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
    monkeypatch.setattr(caching_decorators, "cache", _DummyCache())
