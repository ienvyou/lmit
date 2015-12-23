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
        logger.info("This is not a window. Try to load curses panel and textpad")
        import curses
        import curses.panel
        from curses.textpad import Textbox
    except ImportError:
        logger.critical(
            "Curses module not found. LMIT cannot start in standalone mode.")
        sys.exit(1)
else:
    logger.info("lmit_colorconsole import succeed. Initialize the screen")
    from lmit.ui.lmit_colorconsole import WCurseLight
    curses = WCurseLight()

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

        # Init colors
        self.hascolors = False
        if curses.has_colors() and curses.COLOR_PAIRS > 8:
            self.hascolors = True
            # FG color, BG color
            if args.theme_white:
                curses.init_pair(1, curses.COLOR_BLACK, -1)
            else:
                curses.init_pair(1, curses.COLOR_WHITE, -1)
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
            curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
            curses.init_pair(6, curses.COLOR_RED, -1)
            curses.init_pair(7, curses.COLOR_GREEN, -1)
            curses.init_pair(8, curses.COLOR_BLUE, -1)
            try:
                curses.init_pair(9, curses.COLOR_MAGENTA, -1)
            except Exception:
                if args.theme_white:
                    curses.init_pair(9, curses.COLOR_BLACK, -1)
                else:
                    curses.init_pair(9, curses.COLOR_WHITE, -1)
            try:
                curses.init_pair(10, curses.COLOR_CYAN, -1)
            except Exception:
                if args.theme_white:
                    curses.init_pair(10, curses.COLOR_BLACK, -1)
                else:
                    curses.init_pair(10, curses.COLOR_WHITE, -1)

        else:
            self.hascolors = False

        A_BOLD = curses.A_BOLD

        self.title_color = A_BOLD
        self.title_underline_color = A_BOLD | curses.A_UNDERLINE
        self.help_color = A_BOLD

        """ Configure color attr """

        # Init main window
        self.term_window = self.screen.subwin(0, 0)

        # Init edit filter tag
        self.edit_filter = False

        # Catch key pressed with non blocking mode
        self.no_flash_cursor()
        self.term_window.nodelay(1)
        self.pressedkey = -1

        """
        self.term_window.border(0)
        self.term_window.addstr(2, 2, "Please enter a number...")
        self.term_window.refresh()
        #self.screen.refresh()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.screen.keypad(1)
        self.screen.bkgd(curses.color_pair(2))
        self.screen.refresh()

        self.screen.border(0)
        self.screen.addstr(2, 2, "Please enter a number...")
	self.screen.addstr(4, 4, "1 - Add a user")
	self.screen.addstr(5, 4, "2 - Restart Apache")
	self.screen.addstr(6, 4, "3 - Show disk space")
	self.screen.addstr(7, 4, "4 - Exit")
	self.screen.refresh()
        """

    def flash_cursor(self):
        self.term_window.keypad(1)

    def no_flash_cursor(self):
        self.term_window.keypad(0)

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

    def erase(self):
        """Erase the content of the screen."""
        self.term_window.erase()

    def init_line_column(self):
        """Init the line and column position for the curses inteface."""
        self.init_line()
        self.init_column()

    def init_line(self):
        """Init the line position for the curses inteface."""
        self.line = 0
        self.next_line = 0

    def init_column(self):
        """Init the column position for the curses inteface."""
        self.column = 0
        self.next_column = 0

    def flush(self, stats, cs_status=None):
        """Clear and update the screen.
        stats: Stats database to display
        cs_status:
            "None": standalone or server mode
            "Connected": Client is connected to the server
            "Disconnected": Client is disconnected from the server
        """
        self.erase()
        self.display(stats, cs_status=cs_status)

    def display(self, stats, cs_status=None):
        """Display stats on the screen.
        stats: Stats database to display
        cs_status:
            "None": standalone or server mode
            "Connected": Client is connected to a Glances server
            "SNMP": Client is connected to a SNMP server
            "Disconnected": Client is disconnected from the server
        Return:
            True if the stats have been displayed
            False if the help have been displayed
        """
        # Init the internal line/column for Glances Curses
        self.init_line_column()

        # Get the screen size
        screen_x = self.screen.getmaxyx()[1]
        screen_y = self.screen.getmaxyx()[0]

        logger.debug('Screen size x: {0}, y: {1}'.format(screen_x, screen_y))

        # Display LMIT menu using curses interface
        ############################################
        
        # Help screen
        if self.args.help_tag:
            # Display help plugin 
            return False

    def get_key(self, window):
        # Catch ESC key AND numlock key (issue #163)
        keycode = [0, 0]
        keycode[0] = window.getch()
        keycode[1] = window.getch()

        if keycode != [-1, -1]:
            logger.debug("Keypressed (code: %s)" % keycode)

        if keycode[0] == 27 and keycode[1] != -1:
            # Do not escape on specials keys
            return -1
        else:
            return keycode[0]

    def __catch_key(self, return_to_browser=False):
        # Catch the pressed key
        self.pressedkey = self.get_key(self.term_window)

        # Actions
        if self.pressedkey == ord('\x1b') or self.pressedkey == ord('q'):
            # 'ESC'|'q' > Quit
            self.end()
            logger.info("Stop LMIT client browser")
            sys.exit(0)

    def update(self, stats, cs_status=None, return_to_browser=False):
        """ Update the screen

        Wait for __refresh_time sec / catch key every 100 ms.
        INPUT
        stats: Stats database to display
        cs_status:
            "None": standalone or server mode
            "Connected": Client is connected to the server
            "Disconnected": Client is disconnected from the server
        return_to_browser:
            True: Do not exist, return to the browser list
            False: Exit and return to the shell
        OUPUT
        True: Exit key has been pressed
        False: Others cases...
        """
        # Flush display
        self.flush(stats, cs_status=cs_status)

        # Wait key
        exitkey = False
        while not exitkey:
            # Get key
            pressedkey = self.__catch_key(return_to_browser=return_to_browser)
            # Is it an exit key?
            exitkey = (pressedkey == ord('\x1b') or pressedkey == ord('q'))
            if not exitkey and pressedkey > -1:
                # Redraw display
                self.flush(stats, cs_status=cs_status)

            # Wait 100ms
            curses.napms(100)

        return exitkey

class LmitCursesStandalone(_LmitCurses):

    """Class for the LMIT curse standalone."""

    pass


