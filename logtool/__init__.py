#! /usr/bin/env python

import pyver
__version__, __version_info__ = pyver.get_version (pkg = __name__)
from logtool.log_wrap import log_func
from logtool.log_fault_impl import log_fault
