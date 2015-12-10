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
    refresh_time = 3

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
        
        # Client/Server option
        parser.add_argument('-c', '--client', dest='client',
                            help='connect to a LMIT server by IPv4/IPv6 address or hostname')
        parser.add_argument('-s', '--server', action='store_true', default=False,
                            dest='server', help='run LMIT in server mode')
        parser.add_argument('-t', '--time', default=self.refresh_time, type=float,
                            dest='time', help='set refresh time in seconds [default: {0} sec]'.format(self.refresh_time))

        # Display options
        parser.add_argument('-q', '--quiet', default=False, action='store_true',
                            dest='quiet', help='do not display the curses interface')

        return parser

    def parse_args(self):
        """Parse command line arguments."""
        args = self.init_args().parse_args()

        # Load the configuration file, if it exists
        self.config = Config(args.conf_file)

        # Debug mode
        if args.debug:
            print "Setting logging level to DEBUG"
            from logging import DEBUG
            logger.setLevel(DEBUG)
       
        # Contreol parameter and exit if it is not OK
        self.args = args 

        return args

    def is_standalone(self):
        """ Return True if LMIT is running in standalone mode."""
        return not self.args.client and not self.args.server 

    def is_client(self):
        """ Return True if LMIT is running in client mode."""
        return self.args.client and not self.args.server

    def is_server(self):
        """Return True if LMIT is running in server mode."""
        return not self.args.client and self.args.server

    def get_config(self):
        """Return configuration file object."""
        return self.config

    def get_args(self):
        """Return the arguments"""
        return self.args
