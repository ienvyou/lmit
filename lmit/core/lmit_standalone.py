"""Manage the LMIT standalone session."""

from time import sleep

from lmit.core.lmit_stats import LmitStats
from lmit.core.lmit_logging import logger
from lmit.ui.lmit_curses import LmitCursesStandalone

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

    def __serve_forever(self):
        """ Main loop for CLI """
        while True:
            # Update system information
            #self.stats.update()
           
            if not self.quiet:
                # Update screen
                self.screen.update(self.stats)
            else:
                # Wait...
                sleep(self.refresh_time)
            # Export stats using export modules
            #self.stats.export(self.stats)

    def serve_forever(self):
        """ Wrapper to serve forever function
        This function will restore the terminal to a sane state
        before re-raising the exception and generating a traceback.
        """ 
        try:
            return self.__serve_forever()
        finally: 
            self.end()

    def end(self):
        """End of the standalone CLI."""
        if not self.quiet:
            logger.info("End of standalone mode screen")
            self.screen.end()

        # Exit from export modules
        self.stats.end()
