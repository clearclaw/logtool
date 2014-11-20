#! /usr/bin/env python

import inspect, linecache, logging, os, sys, time, wrapt

# logging.basicConfig (level = logging.INFO)
LOG = logging.getLogger (__name__)

@wrapt.decorator
def log_func_noargs (fn, instance, args, kwargs):
  if LOG.isEnabledFor (logging.DEBUG):
    LOG.debug (
      "Called: %s:%s:%s (...)",
      fn.__class__.__name__, fn.__module__, fn.__name__)
  tic = time.time ()
  rc = fn (*args, **kwargs)
  toc = time.time ()
  if LOG.isEnabledFor (logging.DEBUG):
    LOG.debug (
      "Return: %s:%s:%s (...)  Duration: %.6f secs",
      fn.__class__.__name__, fn.__module__, fn.__name__, toc - tic)
  return rc

@wrapt.decorator
def log_func (fn, instance, *args, **kwargs):
  if LOG.isEnabledFor (logging.DEBUG):
    LOG.debug (
      "Called: %s:%s:%s (%s %s)",
      fn.__class__.__name__, fn.__module__, fn.__name__,
      args, kwargs)
  tic = time.time ()
  rc = fn (*args, **kwargs)
  toc = time.time ()
  if LOG.isEnabledFor (logging.DEBUG):
    LOG.debug (
      "Return: %s:%s:%s (%s %s)  Duration: %.6f secs",
      fn.__class__.__name__, fn.__module__, fn.__name__,
      args, kwargs, toc - tic)
  return rc

class log_trace (object):

  def __init__ (self):
    log_debug = LOG.isEnabledFor (logging.DEBUG)

  def globaltrace (self, frame, why, arg):
    return self.localtrace if why == "call" else None

  def localtrace (self, frame, why, arg):
    if self.log_debug and why in ["c_call", "call", "line"]:
      f_code = frame.f_code
      filename = f_code.co_filename
      funcname = f_code.co_name
      linenum = frame.f_lineno
      fname = os.path.basename (filename)
      LOG.debug ("%s:%s(...) #%s: %s", fname, funcname, linenum,
                 linecache.getline (filename, linenum).rstrip ())
    return self.localtrace

  @wrapt.decorator
  def __call__ (self, fn, instance, args, kwargs):
    sys.settrace (self.globaltrace)
    result = fn (*args, **kwds)
    sys.settrace (None)
    return result

class log_call (log_trace):

  def __init__ (self, log_enter = True, log_args = True, log_exit = True,
                log_rc = True, log_trace = False):
    self.log_enter = log_enter
    self.log_args = log_args
    self.log_exit = log_exit
    self.log_rc = log_rc
    self.log_trace = log_trace

  @wrapt.decorator
  def __call__ (self, fn, instance, args, kwargs):
    argnames = fn.func_code.co_varnames[:fn.func_code.co_argcount]
    log_debug = LOG.isEnabledFor (logging.DEBUG)
    if self.log_enter and log_debug:
      if self.log_args:
        arg_str = ", ".join ("%s=%r" % entry for entry in
                             zip (argnames, args) + kwargs.items ())
      else:
        arg_str = "..."
      LOG.debug ("Called: %s:%s:%s (%s)",
                 fn.__class__.__name__, fn.__module__, fn.__name__, arg_str)
    if self.log_trace:
      sys.settrace (self.globaltrace)
    tic = time.time ()
    rc = fn (*args, **kwargs)
    toc = time.time ()
    if self.log_trace:
      sys.settrace (None)
    if self.log_exit and log_debug:
      LOG.debug (
        "Return: %s:%s:%s (...)  To: %s  Duration: %.6f secs  RC: %s",
        inspect.currentframe ().f_back.f_code.co_name,
        fn.__class__.__name__, fn.__module__, fn.__name__, toc - tic,
        rc if self.log_rc else "...")
    return rc
