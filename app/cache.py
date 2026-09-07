from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


# just a comment to test
def init_cache():
    FastAPICache.init(InMemoryBackend(), prefix= "practice-cache")