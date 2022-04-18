import functools
import time


def deco_status_code(func, default=200):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        return result if result.status_code == default else None

    return wrap


def deco_delay(delay):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(delay)
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
