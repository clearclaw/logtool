#! /usr/bin/env python

import pyver
__version__, __version_info__ = pyver.get_version (pkg = __name__)
from logtool.log_wrap import log_func, log_func_noargs
from logtool.log_fault_impl import log_fault
from logtool.logtime import now, time_str
