""" This is display for Software Installation and Maintenance Menu """

from datetime import datetime

# Import LMIT libs

from lmit.lmit_logger import logger

class SubMenu(object):
    """ LMIT install menu plugin """
    def __init__(self, args=None):
        logger.info("Initialize Security & User menu")

    def process(self):
        logger.info("Security & User Menu Process Start")
