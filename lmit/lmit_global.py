""" Common objects shared by all LMIT modules """

import os
import sys

# Global Information
appname = 'lmit'
version = __import__('lmit').__version__
psutil_version = __import__('lmit').__psutil_version

# Path Definitions
work_path = os.path.realpath(os.path.dirname(__file__))

# Set the plugins path
plugins_path = os.path.realpath(os.path.join(work_path, '..', 'plugins'))

sys_path = sys.path[:]
sys.path.insert(1, plugins_path)
