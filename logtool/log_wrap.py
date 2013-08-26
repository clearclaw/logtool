#! /usr/bin/env python

import logging
from functools import wraps

# logging.basicConfig (level = logging.INFO)
LOG = logging.getLogger (__name__)

def log_func (fn):
  @wraps (fn)
  def wrapper (*args, **kwargs):
    if LOG.isEnabledFor (logging.DEBUG):
      LOG.debug (
        "Entered: %s:%s:%s (%s %s)",
        fn.__class__.__name__, fn.__module__, fn.__name__,
        args, kwargs)
    return fn (*args, **kwargs)
  return wrapper

def log_func2 (fn):
  """This decorator dumps out the arguments passed to a function
  before calling it"""
  argnames = fn.func_code.co_varnames[:fn.func_code.co_argcount]
  fn_str = fn.func_name
  def wrapper (*args, **kwargs):
    LOG.debug ("Entered: %s.%s.%s/%s (%s)",
      fn.__class__.__name__, fn.__module__, fn.__name__, fn_str,
      ', '.join ("%s=%r"
                 % entry for entry in zip (argnames, args) + kwargs.items ()))
    return fn (*args, **kwargs)
  return wrapper
