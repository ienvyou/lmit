"""Manage the configuration file."""

# Import system libs
import os
import sys
try:
    from configparser import ConfigParser
    from configparser import NoOptionError
except ImportError:  # Python 2
    from ConfigParser import SafeConfigParser as ConfigParser
    from ConfigParser import NoOptionError

# Import Glances lib
from lmit.core.lmit_globals import (
    appname,
    is_bsd,
    is_linux,
    is_mac,
    is_py3,
    is_windows,
    sys_prefix
)
from lmit.core.lmit_logging import logger


class Config(object):

    """This class is used to access/read config file, if it exists.
    :param config_dir: the path to search for config file
    :type config_dir: str or None
    """

    def __init__(self, config_dir=None):
        self.config_dir = config_dir
        self.config_filename = 'lmit.conf'
        self._loaded_config_file = None

        self.parser = ConfigParser()

