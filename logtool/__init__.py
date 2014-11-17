#! /usr/bin/env python

import pyver
__version__, __version_info__ = pyver.get_version (pkg = __name__)
from logtool.log_wrap import log_func, log_func_noargs, log_call, log_trace
from logtool.log_fault_impl import log_fault, log_fault_exc_str, log_fault_info_str
from logtool.logtime import now, time_str
