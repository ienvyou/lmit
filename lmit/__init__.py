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
from lmit_logger import logger
from lmit_main import LmitMain

try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    print("Warning: Unable to set locale. Expect encoding problems.")

# Check Python version
if sys.version_info < (2, 6) or (3, 0) <= sys.version_info < (3, 3):
    print('LMIT requires at least Python 2.6 or 3.3 to run.')
    sys.exit(1)

# Check PSutil version
psutil_min_version = (2, 0, 0)
psutil_version = tuple([int(num) for num in __psutil_version.split('.')])

if psutil_version < psutil_min_version:
    print('PSutil 2.0 or higher is needed. LMIT cannot start.')
    sys.exit(1)

def __signal_handler(signal, frame):
    """Callback for CTRL-C."""
    core.end()
    end()

def end():
    """Stop LMIT."""
    logger.info("Stop LMIT(with CTRL-C)")

    # End
    sys.exit(0)


def main():
    # Log LMIT and PSutil version
    logger.info('Start LMIT {0}'.format(__version__))
    logger.info('{0} {1} and PSutil {2} detected'.format(
        platform.python_implementation(),
        platform.python_version(),
        __psutil_version))

    # Share global var
    global core

    # Create the LMIT main instance
    core = LmitMain()

    # Catch the CTRL-C signal
    signal.signal(signal.SIGINT, __signal_handler)

    # Load Plug-In directory
    core.getAllPlugins()

    core.process()
