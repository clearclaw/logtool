#! /usr/bin/env python

from __future__ import absolute_import

from ._version import get_versions
__version__ = get_versions()['version']
__version_info__ = get_versions ()
del get_versions

from .log_wrap import log_func, log_func_noargs, log_call, log_trace
from .log_fault_impl import log_fault, log_fault_exc_str
from .log_fault_impl import log_fault_einfo, log_fault_info_str
from .logtime import now, time_str
