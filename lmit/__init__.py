# -*- coding: utf-8 -*-
#
# This file is part of LMIT.
#
# Copyright (C) 2015 Ji-Woong Choi<jchoi@osci.kr>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""Init the LMIT software."""

__appname__ = 'lmit'
__version__ = '0.0.1'
__author__ = 'Ji-Woong Choi<jchoi@osci.kr>'
__license__ = 'GPL'

# Import system lib
import locale
import platform
import signal
import sys

print "Start importing psutil library"

# Import psutil
try:
    from psutil import __version__ as __psutil_version
    print('PSutil library is loaded. Start LMIT.')
except ImportError:
    print('PSutil library not found. LMIT cannot start.')
    sys.exit(1)

# Import LMIT libs
# Note: others LMIT libs will be imported optionally
from lmit.core.lmit_logging import logger
from lmit.core.lmit_main import LmitMain

try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    print("Warning: Unable to set locale. Expect encoding problems.")

# Check Python version
if sys.version_info < (2, 6) or (3, 0) <= sys.version_info < (3, 3):
    print('Glances requires at least Python 2.6 or 3.3 to run.')
    sys.exit(1)

# Check PSutil version
psutil_min_version = (2, 0, 0)
psutil_version = tuple([int(num) for num in __psutil_version.split('.')])

if psutil_version < psutil_min_version:
    print('PSutil 2.0 or higher is needed. Glances cannot start.')
    sys.exit(1)

def __signal_handler(signal, frame):
    """Callback for CTRL-C."""
    end()

def end():
    """Stop Glances."""
    logger.info("Stop LMIT(with CTRL-C)")

def main():
    # Log LMIT and PSutil version
    logger.info('Start Glances {0}'.format(__version__))
    logger.info('{0} {1} and PSutil {2} detected'.format(
        platform.python_implementation(),
        platform.python_version(),
        __psutil_version))

    # Share global var
    global core, standalone, client, server, webserver
    
    # Create the Glances main instance
    core = LmitMain()

    # Catch the CTRL-C signal
    signal.signal(signal.SIGINT, __signal_handler)
