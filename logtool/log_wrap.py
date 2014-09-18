#! /usr/bin/env python

import logging
from functools import wraps

# logging.basicConfig (level = logging.INFO)
LOG = logging.getLogger (__name__)

def log_func_noargs (fn):
  @wraps (fn)
  def wrapper_noargs (*args, **kwargs):
    if LOG.isEnabledFor (logging.DEBUG):
      LOG.debug (
        "Entered: %s:%s:%s (...)",
        fn.__class__.__name__, fn.__module__, fn.__name__)
    return fn (*args, **kwargs)
  return wrapper_noargs

def log_func (fn):
  @wraps (fn)
  def wrapper_args (*args, **kwargs):
    if LOG.isEnabledFor (logging.DEBUG):
      LOG.debug (
        "Entered: %s:%s:%s (%s %s)",
        fn.__class__.__name__, fn.__module__, fn.__name__,
        args, kwargs)
    return fn (*args, **kwargs)
  return wrapper_args
