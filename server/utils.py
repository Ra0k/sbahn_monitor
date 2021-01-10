import datetime
from datetime import datetime
from typing import Any, Callable


def get_env(name):
    import os
    env = os.environ.get(name, None)
    if env is None:
        raise Exception('{} env variable is not found.'.format(name))
    return env


def diff_datetime(datetime1, datetime2):
    return abs(datetime2 - datetime1).seconds


convert_timestamp: Callable[[Any], datetime] = lambda x: datetime.datetime.fromtimestamp(x / 1e3)


def raise_message(message, include_original=True):
    def real_decorator(method):
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                if include_original:
                    raise Exception('{} \n{}'.format(message, e))
                else:
                    raise Exception(message)

        return wrapper

    return real_decorator
