"""The stats manager."""

import collections
import os
import re
import sys
import threading

from lmit.core.lmit_globals import exports_path, plugins_path, sys_path
from lmit.core.lmit_logging import logger

class LmitStats(object):
    """This class stores, updates and gives stats."""

    def __init__(self, config=None, args=None):
        # Set the argument instance
        self.args = args

        # Set the config instance
        self.config = config
