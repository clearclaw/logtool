logtool
=======

Methods and tools that assist logging.

log\_func
---------

A decorator for function and method definitions that logs at DEBUG level
every call to that function or method along with its arguments.

eg

::

    @logtool.log_wrap
    def my_method (self, *args):
      ...stuff here...

Resulting log entry from a real production usage (with a few of the
argumentvalues redacted):

::

    Entered: function:test_tool.toolwrapper:email_report ((<test_tool.meshtool.Wrapper object at 0x7f19d4879c10>, path(u'../file.ext'), 'address@domain.com', 'address@domain.com', 'Interesting subject header') {})

The {} at the end shows that there were no named arguments passed to
that call, else they would be shown there.

log\_func\_noargs
-----------------

A decorator for function and method definitions that logs at DEBUG level
every call to that function or method but without any arguments. This
can be useful when traversing and dumping the arguments would be
execssively expensive, or would potentially create infinite loops.

eg

::

    @logtool.log_wrap_noargs
    def my_method (self, *args):
      ...stuff here...

log\_fault
----------

Logs an exception in a standardised form, including the source file and
line number of the exception, and if logging at DEBUG level, also logs a
stack trace along with all the variables in each stack frame. eg

In WARN or high mode:

::

    CRITICAL <log_fault_impl:log_fault(24)> FAULT: /usr/local/lib/python2.7/dist-packages/workerd-0.1.26_gbb342e2-py2.7.egg/workerd/do.py(243): IOError(28, 'No space left on device')

When logging at DEBUG:

::

    CRITICAL <log_fault_impl:log_fault(24)> FAULT: /usr/local/lib/python2.7/dist-packages/workerd-0.1.26_gbb342e2-py2.7.egg/workerd/do.py(243): IOError(28, 'No space left on device')
    DEBUG <log_fault_impl:log_fault(26)> Locals by frame, innermost last:
    DEBUG <log_fault_impl:log_fault(30)> Frame run in /usr/local/lib/python2.7/dist-packages/workerd-0.1.26_gbb342e2-py2.7.egg/workerd/do.py at line 248
    DEBUG <log_fault_impl:log_fault(40)>                 self = <workerd.do.Do object at 0x7f5709e3d490>
    DEBUG <log_fault_impl:log_fault(40)>                    e = [Errno 28] No space left on device
    DEBUG <log_fault_impl:log_fault(40)>                   rc = 0
    DEBUG <log_fault_impl:log_fault(30)> Frame wrapper_args in build/bdist.linux-x86_64/egg/mppy/log_wrap.py at line 27
    DEBUG <log_fault_impl:log_fault(40)>                 args = (<workerd.do.Do object at 0x7f5709e3d490>,)
    DEBUG <log_fault_impl:log_fault(40)>                   fn = <function do_job at 0x7f570a2936e0>
    DEBUG <log_fault_impl:log_fault(40)>               kwargs = {}
    DEBUG <log_fault_impl:log_fault(30)> Frame do_job in /usr/local/lib/python2.7/dist-packages/workerd-0.1.26_gbb342e2-py2.7.egg/workerd/do.py at line 227
    DEBUG <log_fault_impl:log_fault(40)>                  toc = 1410867312.58
    DEBUG <log_fault_impl:log_fault(40)>                 self = <workerd.do.Do object at 0x7f5709e3d490>
    DEBUG <log_fault_impl:log_fault(40)>                  tic = 1410842559.54
    DEBUG <log_fault_impl:log_fault(40)>                   rc = -99
    DEBUG <log_fault_impl:log_fault(30)> Frame __setitem__ in build/bdist.linux-x86_64/egg/mppy/jsondict.py at line 69
    DEBUG <log_fault_impl:log_fault(40)>                 self = {u'status': u'pending', u'notified_for': u'pending
    DEBUG <log_fault_impl:log_fault(40)>                  key = execution_time
    DEBUG <log_fault_impl:log_fault(40)>                  val = 24753.043578
    DEBUG <log_fault_impl:log_fault(40)>               kwargs = {}
    DEBUG <log_fault_impl:log_fault(30)> Frame wrapper in build/bdist.linux-x86_64/egg/mppy/jsondict.py at line 80
    DEBUG <log_fault_impl:log_fault(40)>                 self = {u'status': u'pending', u'notified_for': u'pending
    DEBUG <log_fault_impl:log_fault(40)>               kwargs = {}
    DEBUG <log_fault_impl:log_fault(40)>                 attr = <bound method JsonDict.save of {u'status': u'pendi
    DEBUG <log_fault_impl:log_fault(40)>                 args = ()
    DEBUG <log_fault_impl:log_fault(40)>           was_loaded = True
    DEBUG <log_fault_impl:log_fault(30)> Frame save in build/bdist.linux-x86_64/egg/mppy/jsondict.py at line 46
    DEBUG <log_fault_impl:log_fault(40)>                force = False
    DEBUG <log_fault_impl:log_fault(40)>                 self = {u'status': u'pending', u'notified_for': u'pending
    DEBUG <log_fault_impl:log_fault(40)>                   fd = 5
    DEBUG <log_fault_impl:log_fault(40)>                   fn = /var/spool/matterport/workerd/generate_mesh/d34fea

time\_str
---------

Simply returns a time\_t (seconds since the epoch, possibly fractional)
in a simple consistent string form suitable for logfiles, reports and
the like.

See below under ``now`` for an example.

now
---

Reurns a tuple of the current time as a time\_t, and its matching
time\_str. Getting the two together allows the string to be used for
logs and the like, and the time_t to be used as a numeric.  eg:

::

    $ ipython
    Python 2.7.6 (default, Mar 22 2014, 22:59:56)
    Type "copyright", "credits" or "license" for more information.

    IPython 1.2.1 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.

    In [1]: import logtool

    In [2]: logtool.now ()
    Out[2]: (1411075417, '21:23:37 Thu 18 Sep 2014 Z+0000')

    In [3]: logtool.time_str (logtool.now ()[0])
    Out[3]: '14:23:42 Thu 18 Sep 2014 Z+0000'
