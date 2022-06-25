import functools
import time

__all__ = (
    'deco_status_code',
    'deco_delay',
)


def deco_status_code(expected_code):
    def decorator(func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            result = func(*args, **kwargs)
            return result if result.status_code == expected_code else None

        return wrap

    return decorator


def deco_delay(delay):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(delay)
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
