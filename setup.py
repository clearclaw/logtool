#! /usr/bin/env python

from setuptools import setup, find_packages
import versioneer
from codecs import open

setup (
    name = "logtool",
    version = versioneer.get_version (),
    description = "Methods and tools that assist logging.",
    long_description = open ("README.rst", 'r', encoding = 'utf-8').read (),
    cmdclass = versioneer.get_cmdclass (),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        + "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Utilities",
    ],
    keywords = "logging, exceptions, callpoints, call tracing",
    author = "J C Lawrence",
    author_email = "claw@kanga.nu",
    url = "https://github.com/clearclaw/logtool",
    license = "LGPL v3.0",
    test_suite = "tests",
    packages = find_packages (exclude = ["tests",]),
    package_data = {},
    data_files = [],
    zip_safe = False,
    install_requires = [line.strip ()
        for line in open ("requirements.txt", 'r',
                          encoding = 'utf-8').readlines ()],
    entry_points = {
        "console_scripts": [
        ],
    },
)
