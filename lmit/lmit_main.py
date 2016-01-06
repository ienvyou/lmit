import sys
import time
import curses
import curses.panel
from curses.textpad import Textbox
from lmit_logger import logger


menu_item = {
    'title': "Move cursor to desired item and press Enter",
    'items':[
        { 'menu': "Software Installation and Maintenance" },    
        { 'menu': "Software License Management" },    
        { 'menu': "Devices" },    
        { 'menu': "System Storage Management (Physical & Logical Storage)" },    
        { 'menu': "Security & Users" },    
        { 'menu': "Communications Applications and Services" },    
        { 'menu': "Problem Determination" },    
        { 'menu': "System Environments" },    
        { 'menu': "Create OSC Monthly System Check Report" },    
    ]
}

class LmitMain(object):
    """ Draw main menu """

    def __init__(self):
        # Init windows positions
        self.term_w = 80
        self.term_h = 24

        # Self Position
        self.position = 0

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

        A_BOLD = curses.A_BOLD

        self.title_color = A_BOLD
        self.title_underline_color = A_BOLD | curses.A_UNDERLINE
        self.help_color = A_BOLD

        # application does not need a blinking cursor at all
        curses.curs_set(0)

        # Init main window
        self.term_window = self.screen.subwin(0, 0)

        # Init edit filter tag
        self.edit_filter = False

        # Catch key pressed with non blocking mode
        self.term_window.keypad(0)
        self.term_window.nodelay(1)
        self.pressedkey = -1

        self.term_window.erase()

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

    def __catch_key(self):
        # Catch the pressed key
        self.pressedkey = self.get_key(self.term_window)

        # Actions
        if self.pressedkey == ord('\x1b') or self.pressedkey == ord('q'):
            # 'ESC'|'q' > Quit
            self.end()
            logger.info("Stop LMIT by q-key event")
            sys.exit(0)

        return self.pressedkey

    def display(self):
        # Line index
        self.menu_line = 5
        self.menu_column = 5

        # Cursur index
        self.index = 0;

        # Get the screen size
        screen_x = self.screen.getmaxyx()[1]
        screen_y = self.screen.getmaxyx()[0]

        logger.info('Screen size x: {0}, y: {1}'.format(screen_x, screen_y))

        mode = curses.A_REVERSE

        title = "Linux Management Interface Tool(LMIT)"

        title_x = screen_x / 2
        self.term_window.addstr(1, title_x - (len(title)/2), title, curses.A_BOLD)

        self.term_window.addstr(3, 2, menu_item['title'])

        items = menu_item['items']

        for item in items:
            #logger.info('menu name: {0}'.format(item['menu']))
            if self.index == self.position:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL
            
            self.term_window.addstr(self.menu_line + self.index, self.menu_column, item['menu'], mode)
            self.index = self.index + 1

        self.term_window.border(0)
        self.term_window.refresh()

    def process(self):

        # Display first
        self.display()

        # Wait key
        exitkey = False

        while not exitkey:
            # Get key
            pressedkey = self.__catch_key()
            #logger.info('Current pressed key: {0}'.format(self.pressedkey))
            
            # Is it an exit key?
            exitkey = (self.pressedkey == ord('\x1b') or self.pressedkey == ord('q'))
            if not exitkey and self.pressedkey > -1:
                # Pressed key is KEY_UP
                if self.pressedkey == 65:
                    logger.info('Key Up Event')
                    if self.position > 0  :
                        self.position = self.position - 1 
                # Pressed key is KEY_DOWN
                elif self.pressedkey == 66:
                    logger.info('Key Down Event')
                    if self.position < len(menu_item['items']) - 1:
                        self.position = self.position + 1
                # Pressed key is KEY_ENTER 
                elif self.pressedkey == 10:
                    item = menu_item['items'][self.position]
                    logger.info('Enter Key Event - {0}'.format(item['menu']))

                # Redraw display
                self.display()

            # Wait 50ms
            curses.napms(50)
 

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

