
"""Curses interface class."""

# Import system lib
import re
import sys

# Import LMIT lib
from lmit.core.lmit_globals import is_mac, is_windows
from lmit.core.lmit_logging import logger

class _LmitCurses(object):
    """This class manages the curses display(and key pressed)."""

    def __init__(self, args=None):
        logger.info("_LmitCurses __init__ function called")
        # init args
        self.args = args

class LmitCursesStandalone(_LmitCurses):

    """Class for the LMIT curse standalone."""

    pass
