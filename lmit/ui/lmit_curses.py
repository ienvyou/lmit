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

# Import curses lib for "normal" operating system and consolelog for Windows
if not is_windows:
    try:
        import curses
        import curses.panel
        from curses.textpad import Textbox
        print "Curses module found. LMIT will start in standalone mode."
    except ImportError:
#        logger.critical(
#            "Curses module not found. Glances cannot start in standalone mode.")
        print "Curses module not found. LMIT cannot tart in standalone mode."
        sys.exit(1)
#else:
#    from glances.outputs.glances_colorconsole import WCurseLight
#    curses = WCurseLight()
