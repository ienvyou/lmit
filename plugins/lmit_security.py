""" This is display for Software Installation and Maintenance Menu """

from datetime import datetime

# Import LMIT libs

from lmit.lmit_logger import logger

menu_item = {
    'title': "User Mangement",
    'items':[
        { 'key': "user_add", 'menu': "Add a User" },
        { 'key': "change_passwd", 'menu': "Change a User's Password" },
        { 'key': "list_user", 'menu': "List All Users" }
    ]
}


class SubMenu(object):
    """ LMIT install menu plugin """
    def __init__(self, args=None):
        logger.info("Initialize Security & User menu")

    def getMenuItem(self):
        return menu_item

    def process(self):
        logger.info("Security & User Menu Process Start")
