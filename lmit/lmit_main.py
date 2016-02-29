import os
import sys
import time
import collections
from lmit_global import plugins_path, sys_path
from lmit_logger import logger
from lmit_menu import LmitMenu


menu_item = {
    'title': "Move cursor to desired item and press Enter",
    'items':[
        {'key': "install", 'menu': "Software Installation and Maintenance"},
        {'key': "license", 'menu': "Software License Management"},
        {'key': "device", 'menu': "Devices"},
        {'key': "storage", 'menu': "System Storage Management (Physical & Logical Storage)"},
        {'key': "security", 'menu': "Security & Users"},
        {'key': "application", 'menu': "Communications Applications and Services"},
        {'key': "problem", 'menu': "Problem Determination"},
        {'key': "environment", 'menu': "System Environments"},
        {'key': "report", 'menu': "Create OSC Monthly System Check Report"},
    ]
}


class LmitMain(object):
    """ Draw main menu """

    def __init__(self):
        logger.info("Plugins Directory(location: %s)" % plugins_path)
        # Init the plugin list dict
        self._plugins = collections.defaultdict(dict)

        # Load plugins
        self.load_plugins(args=None) 
        
    def load_plugins(self, args=None):
        """ Load all plugins in the 'plugins' directory."""
        header = "lmit_"
        for item in os.listdir(plugins_path):
            if item.startswith(header) and item.endswith(".py"):
                # Import the plugin
                plugin = __import__(os.path.basename(item)[:-3])
                plugin_name = os.path.basename(item)[len(header):-3].lower()

                self._plugins[plugin_name] = plugin.SubMenu(args=args)
        # Log plugin list
        logger.info("Available plugins list: {0}".format(self.getAllPlugins()))

    def getAllPlugins(self):
        """Return the plugins list."""
        return [p for p in self._plugins]

    def process(self):
        logger.info("LMIT Main Process is started")
        
        menu = LmitMenu(menu_item)
        menu.process()

