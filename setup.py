from setuptools import setup, find_packages

__version__ = "unknown"

import pyver
__version__, __version_info__ = pyver.get_version (pkg = "logtool")

setup (name = "logtool",
  version = __version__,
  description = "Methods and tools that assist logging.",
  long_description = "Methods and tools that assist logging.",
  classifiers = [],
  keywords = "",
  author = "J C Lawrence",
  author_email = "claw@kanga.nu",
  url = "http://kanga.nu/~claw/",
  license = "GPL v3.0",
  packages = find_packages (exclude = ["tests",]),
  package_data = {
  },
  zip_safe = True,
  install_requires = [
    "pyver",
  ],
  entry_points = {
    "console_scripts": [
      ],
    },
  )
