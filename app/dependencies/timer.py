import time


def res_time(start: float, end: float) -> str:
  res = end - start
  return time.strftime('%H:%M:%S', time.gmtime(res))
