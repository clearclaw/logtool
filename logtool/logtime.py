#! /usr/bin/env python

import logging
from datetime import datetime
from time import gmtime, strftime, time
from logtool import log_func

DEFAULT_TIMEFORMAT = "%H:%M:%S %a %d %b %Y Z+0000"
DEFAULT_SOLIDFORMAT = "%Y-%m-%d-%H%M.%S-Z0000"

LOG = logging.getLogger (__name__)

@log_func
def time_str (time_t):
  '''Converts floating point number a'la time.time()
  using DEFAULT_TIMEFORMAT
  '''
  return datetime.fromtimestamp (int (time_t)).strftime (DEFAULT_TIMEFORMAT)

@log_func
def now (time_t = None, solid = False):
  '''Gives current time as tuple (t, t_str) where
     t is integer portion from time.time()
     t_str string of t using DEFAULT_TIMEFORMAT
  '''
  if not time_t:
    time_t = time ()
  if not solid:
    time_s = strftime (DEFAULT_TIMEFORMAT, gmtime (time_t))
  else:
    time_s = strftime (DEFAULT_SOLIDFORMAT, gmtime (time_t))
  return (int (time_t), time_s)
