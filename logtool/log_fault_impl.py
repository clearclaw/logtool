#! /usr/bin/env python

import logging, sys
from StringIO import StringIO
from logtool import log_call

# logging.basicConfig (level = logging.INFO)
LOG = logging.getLogger (__name__)

# @log_call ()
def _generate_stackdump (stack):
  yield "Locals by frame, innermost last:"
  for frame in stack:
    yield ("Frame %s in %s at line %s" %(frame.f_code.co_name,
                                         frame.f_code.co_filename,
                                         frame.f_lineno))
    for key, value in frame.f_locals.items ():
      s = "%20s = " % key
      # We have to be careful not to cause a new error in our error
      # printer! Calling str() on an unknown object could cause an
      # error we don't want.
      try:
        s += str (value)[:50] # Trim large strings
      except: # pylint: disable-msg=W0702
        s += "<ERROR WHILE PRINTING VALUE>"
      yield s

# @log_call ()
def _get_stack (tb):
  stack = []
  while tb:
    stack.append (tb.tb_frame)
    tb = tb.tb_next
  return stack

@log_call ()
def log_fault (exc, message = "", level = logging.CRITICAL,
               traceback = False):
  """Print the usual traceback information, followed by a listing of all
  the local variables in each frame.
  """
  tb = sys.exc_info ()[2]
  stack = _get_stack (tb)
  LOG.log (level,
           "FAULT: %s%s(%s): %s", ("%s -- " % message) if message else "",
           tb.tb_frame.f_code.co_filename,
           tb.tb_lineno,
           repr (exc))
  if traceback or LOG.isEnabledFor (logging.DEBUG):
    for line in _generate_stackdump (stack):
      LOG.debug (line)

@log_call ()
def log_fault_exc_str (exc, message = "", level = logging.CRITICAL,
                       traceback = False):
  """Make a StringIO of the usual traceback information, followed by a
  listing of all the local variables in each frame.
  """
  return log_fault_info_str (sys.exc_info (exc), message = message,
                             level = level, traceback = traceback)

@log_call ()
def log_fault_info_str (exc_info, message = "", level = logging.CRITICAL,
                        traceback = False):
  """Make a StringIO of the usual traceback information, followed by a
  listing of all the local variables in each frame.
  """
  tb = sys.exc_info ()[2]
  stack = _get_stack (tb)
  rc = StringIO ()
  rc.write ("%s: FAULT: %s%s(%s): %s\n"
            % (logging.getLevelName (level),
               ("%s -- " % message) if message else "",
               tb.tb_frame.f_code.co_filename,
               tb.tb_lineno,
               repr (exc_info[1])))
  if traceback:
    for line in _generate_stackdump (stack):
      rc.write ("%s\n" % line)
  return rc.getvalue ()
