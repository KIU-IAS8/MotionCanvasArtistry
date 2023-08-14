from diskcache import Cache

cache = Cache("./caching/cache")


def set_cache(key, value, exp_sec):
    cache.set(key, value, expire=exp_sec)


def get_cache(key):
    spheres = cache.get(key)
    if spheres:
        return spheres
    return False
