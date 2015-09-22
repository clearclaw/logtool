#! /usr/bin/env python

from __future__ import absolute_import
import logging
from datetime import datetime
from time import gmtime, strftime, time
from .log_wrap import log_call

DEFAULT_TIMEFORMAT = "%H:%M:%S %a %d %b %Y Z+0000"
DEFAULT_SLUGFORMAT = "%Y-%m-%d_%H%M.%S"

LOG = logging.getLogger (__name__)

@log_call
def time_str (time_t, slug = False):
  '''Converts floating point number a'la time.time()
  using DEFAULT_TIMEFORMAT
  '''
  return datetime.fromtimestamp (int (time_t)).strftime (
    DEFAULT_SLUGFORMAT if slug else DEFAULT_TIMEFORMAT)

@log_call
def now (time_t = None, slug = False):
  '''Gives current time as tuple (t, t_str) where
     t is integer portion from time.time()
     t_str string of t using DEFAULT_TIMEFORMAT
  '''
  if not time_t:
    time_t = time ()
  time_s = strftime (
    DEFAULT_SLUGFORMAT if slug else DEFAULT_TIMEFORMAT,
    gmtime (time_t))
  return (int (time_t), time_s)
