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

"""Curses interface class."""

# Import system lib
import re
import sys

# Import LMIT lib
from lmit.core.lmit_globals import is_mac, is_windows
from lmit.core.lmit_logging import logger

# Import curses lib for "normal" operating system and consolelog for Windows
if not is_windows:
    try:
        import curses
        import curses.panel
        from curses.textpad import Textbox
    except ImportError:
        logger.critical(
            "Curses module not found. LMIT cannot start in standalone mode.")
        sys.exit(1)
#else:
#    from lmit.outputs.glances_colorconsole import WCurseLight
#    curses = WCurseLight()

class _LmitCurses(object):
    """This class manages the curses display(and key pressed)."""

    def __init__(self, args=None):
        logger.info("_LmitCurses __init__ function called")
        # init args
        self.args = args

        # Init windows positions
        self.term_w = 80
        self.term_h = 24

        # Space between stats
        self.space_between_column = 3
        self.space_between_line = 2

        # Init the curses screen
        self.screen = curses.initscr()
        if not self.screen:
            logger.critical("Cannot init the curses library\n")
            sys.exit(1)

        # Set curses options
        if hasattr(curses, 'start_color'):
            curses.start_color()
        if hasattr(curses, 'use_default_colors'):
            curses.use_default_colors()
        if hasattr(curses, 'noecho'):
            curses.noecho()
        if hasattr(curses, 'cbreak'):
            curses.cbreak()
        self.set_cursor(0)

        """ Configure color attr """

        # Init main window
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.screen.keypad(1)
        self.screen.bkgd(curses.color_pair(2))
        self.screen.refresh()

    def set_cursor(self, value):
        """Configure the curse cursor apparence.
        0: invisible
        1: visible
        2: very visible
        """
        if hasattr(curses, 'curs_set'):
            try:
                curses.curs_set(value)
            except Exception:
                pass

    def end(self):
        """Shutdown the curses window."""
        if hasattr(curses, 'echo'):
            curses.echo()
        if hasattr(curses, 'nocbreak'):
            curses.nocbreak()
        if hasattr(curses, 'curs_set'):
            try:
                curses.curs_set(1)
            except Exception:
                pass
        curses.endwin()


class LmitCursesStandalone(_LmitCurses):

    """Class for the LMIT curse standalone."""

    pass


