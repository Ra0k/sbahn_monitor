def get_env(name):
  import os
  env = os.environ.get(name, None)
  if env is None:
    raise Exception('{} env variable is not found.'.format(name))
  return env


def diff_datetime(datetime1, datetime2):
    return abs(datetime2-datetime1).seconds
