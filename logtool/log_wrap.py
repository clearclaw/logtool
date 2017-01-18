#! /usr/bin/env python

from __future__ import absolute_import
import inspect, linecache, logging, os, six, sys, timeit, wrapt

# logging.basicConfig (level = logging.INFO)
LOG = logging.getLogger (__name__)

@wrapt.decorator
def log_func_noargs (fn, instance, args, kwargs): # pylint: disable=W0613
  if LOG.isEnabledFor (logging.DEBUG):
    LOG.debug (
      "Called: %s:%s:%s (...)",
      fn.__class__.__name__, fn.__module__, fn.__name__)
  tic = timeit.default_timer ()
  rc = fn (*args, **kwargs)
  toc = timeit.default_timer ()
  if LOG.isEnabledFor (logging.DEBUG):
    LOG.debug (
      "Return: %s:%s:%s (...)  Duration: %.6f secs",
      fn.__class__.__name__, fn.__module__, fn.__name__, toc - tic)
  return rc

@wrapt.decorator
def log_func (fn, instance, *args, **kwargs): # pylint: disable=W0613
  if LOG.isEnabledFor (logging.DEBUG):
    LOG.debug (
      "Called: %s:%s:%s (%s %s)",
      fn.__class__.__name__, fn.__module__, fn.__name__,
      args, kwargs)
  tic = timeit.default_timer ()
  rc = fn (*args, **kwargs)
  toc = timeit.default_timer ()
  if LOG.isEnabledFor (logging.DEBUG):
    LOG.debug (
      "Return: %s:%s:%s (%s %s)  Duration: %.6f secs",
      fn.__class__.__name__, fn.__module__, fn.__name__,
      args, kwargs, toc - tic)
  return rc

class log_trace (object):

  def __init__ (self):
    self.log_debug = LOG.isEnabledFor (logging.DEBUG)

  def globaltrace (self, frame, why, arg): # pylint: disable=W0613
    return self.localtrace if why == "call" else None

  def localtrace (self, frame, why, args):
    if self.log_debug and why in ["c_call", "call", "exception", "line",]:
      f_code = frame.f_code
      filename = f_code.co_filename
      funcname = f_code.co_name
      linenum = frame.f_lineno
      fname = os.path.basename (filename)
      exc = ("-- EXCEPTION: %s %s" % (args[0], args[1])
             if why == "exception" else "")
      LOG.debug ("%s:%s(...) #%s: %s %s", fname, funcname, linenum,
                 linecache.getline (filename, linenum).rstrip (), exc)
    return self.localtrace

  @wrapt.decorator
  def __call__ (self, fn, instance, args, kwargs):
    sys.settrace (self.globaltrace)
    result = fn (*args, **kwargs)
    sys.settrace (None)
    return result

@wrapt.decorator
class log_call (log_trace):

  def __init__ ( # pylint: disable=W0231
      self, log_enter = True, log_args = True, log_exit = True,
      log_rc = True, log_exc = False, log_trace = False, # pylint: disable=W0621
      log_level = logging.DEBUG):
    self.log_debug = LOG.isEnabledFor (logging.DEBUG)
    self.log_enter = log_enter
    self.log_args = log_args
    self.log_exit = log_exit
    self.log_rc = log_rc
    self.log_trace = log_trace
    self.log_level = log_level
    self.log_exc = log_exc

  def __call__ (self, fn, instance, args, kwargs):
    log_this = LOG.isEnabledFor (self.log_level)
    if self.log_enter and log_this:
      # Non-python methods don't have a func_code
      if self.log_args and hasattr (fn, "func_code"):
        code = six.get_function_code(fn)
        argnames = code.co_varnames[:code.co_argcount]
        x_args = args if not instance else ((instance,) + args)
        arg_str = ", ".join ("%s=%r" % entry for entry in
                             list(zip (argnames, x_args))
                             + list(kwargs.items ()))
      else: # Why?
        arg_str = "..."
      LOG.log (self.log_level, "Called: %s:%s:%s (%s)",
               fn.__class__.__name__,
               getattr (fn, "__module__", "<?module?>"),
               getattr (fn, "__name__", "<?name?>"),
               arg_str)
    if self.log_trace:
      sys.settrace (self.globaltrace)
    tic = timeit.default_timer ()
    try:
      rc = fn (*args, **kwargs)
    except Exception as e:
      if self.log_exc:
        from .log_fault_impl import log_fault
        log_fault (e)
      raise
    toc = timeit.default_timer ()
    if self.log_trace:
      sys.settrace (None)
    if self.log_exit and log_this:
      LOG.log (
        self.log_level,
        "Return: %s:%s:%s (...) -> %s (...)  Duration: %.6f secs  RC: %r",
        fn.__class__.__name__,
        getattr (fn, "__module__", "<?module?>"),
        getattr (fn, "__name__", "<?name?>"),
        inspect.currentframe ().f_back.f_code.co_name,
        toc - tic, rc if self.log_rc else "...")
    return rc
