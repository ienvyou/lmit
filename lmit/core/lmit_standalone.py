"""Manage the LMIT standalone session."""

from time import sleep

from lmit.core.lmit_stats import LmitStats
from lmit.core.lmit_curses import LmitCursesStandalone

class LmitStandalone(object):
    """This class creates and manages the LMIT standalone session."""

    def __init__(self, config=None, args=None):
        # Quite mode
        self._quiet = args.quiet
        self.refresh_time = args.time

        # Init stats
        self.stats = LmitStats(config=config, args=args)

        if self.quiet:
            logger.info("Quiet mode is ON: Nothing will be displayed on screen")
            # In quiet mode, hothing is displayed
        else:
            self.screen = LmitCursesStandalone(args=args)

    @property
    def quiet(self):
        return self._quiet

    
