#! /usr/bin/env python

import logging, sys
from logtool import log_func

# logging.basicConfig (level = logging.INFO)
LOG = logging.getLogger (__name__)

@log_func
def log_fault (exc, message = "", level = logging.CRITICAL):
  """Print the usual traceback information, followed by a listing of all the
  local variables in each frame."""
  tb = sys.exc_info()[2]
  stack = []
  while tb:
    stack.append (tb.tb_frame)
    tb = tb.tb_next
  # LOG.error ("FAULT: %s -- %s: %s" % (message, etype, edata))
  tb = sys.exc_info ()[2]
  LOG.log (level,
           "FAULT: %s%s(%s): %s", ("%s -- " % message) if message else "",
           tb.tb_frame.f_code.co_filename,
           tb.tb_lineno,
           repr (exc))
  if LOG.isEnabledFor (logging.DEBUG):
    LOG.debug ("Locals by frame, innermost last:")
    for frame in stack:
      LOG.debug ("Frame %s in %s at line %s", frame.f_code.co_name,
                                              frame.f_code.co_filename,
                                              frame.f_lineno)
      for key, value in frame.f_locals.items ():
        s = "%20s = " % key
        # We have to be careful not to cause a new error in our error
        # printer! Calling str() on an unknown object could cause an
        # error we don't want.
        try:
          s += str (value)[:50] # Trim large strings
        except: # pylint: disable-msg=W0702
          s += "<ERROR WHILE PRINTING VALUE>"
        LOG.debug (s)
