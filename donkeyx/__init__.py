import os

import pkg_resources  # part of setuptools
import sys

__version__ = pkg_resources.require("donkeyx")[0].version
print('using donkeyx version: {} ...'.format(__version__))



current_module = sys.modules[__name__]


if sys.version_info.major < 3:
    msg = 'donkeyx Requires Python 3.4 or greater. You are using {}'.format(sys.version)
    raise ValueError(msg)

from . import parts
from .vehicle import Vehicle
from .memory import Memory
from . import util
from . import config
from .config import load_config
