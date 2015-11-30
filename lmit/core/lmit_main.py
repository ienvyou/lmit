""" LMIT main class"""

# Import system libs
import argparse
import os
import sys
import tempfile

# Import LMIT libs
from lmit.core.lmit_config import Config
from lmit.core.lmit_globals import appname, is_linux, is_windows, psutil_version, version
from lmit.core.lmit_logging import logger

class LmitMain(object):
    """ Main class to manage Lmit instance."""
    
    # Default stats' refresh time is 3 seconds

    # Exemple of use
    example_of_use = "\
Examples of use:\n\
\n\
Manage local machine (standalone mode):\n\
  $ lmit\n\
\n\
Monitor local machine and export stats to a CSV file (standalone mode):\n\
  $ lmit --export-csv\n\
\n\
Monitor local machine and export stats to a InfluxDB server with 5s refresh time (standalone mode):\n\
  $ lmit -t 5 --export-influxdb\n\
    "

    def __init__(self):
        """Manage the command line arguments."""
        logger.info("Function __init__ called in LmitMain class in lmit_main.py")
        self.args = self.parse_args()

    def init_args(self):
        """Init all the command line arguments."""
        logger.info("Function init_args called in LmitMain class in lmit_main.py")
        _version = "Glances v" + version + " with psutil v" + psutil_version

        parser = argparse.ArgumentParser(
            prog = appname,
            conflict_handler = 'resolve',
            formatter_class = argparse.RawDescriptionHelpFormatter,
            epilog = self.example_of_use)

        parser.add_argument(
            '-V', '--version', action='version', version=_version)
        parser.add_argument('-d', '--debug', action='store_true', default=False,
                            dest='debug', help='enable debug mode')
        parser.add_argument('-C', '--config', dest='conf_file',
                            help='path to the configuration file')

        return parser

    def parse_args(self):
        """Parse command line arguments."""
        args = self.init_args().parse_args()

        # Load the configuration file, if it exists
        self.config = Config(args.conf_file)
