
"""Custom logging class."""

import logging
try:
    # Python 2.6
    from logutils.dictconfig import dictConfig
except ImportError:
    # Python >= 2.7
    from logging.config import dictConfig
import os
import tempfile

# Define the logging configuration
LOGGING_CFG = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'console']
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s -- %(levelname)s -- %(message)s'
        },
        'short': {
            'format': '%(levelname)s: %(message)s'
        },
        'free': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            # http://stackoverflow.com/questions/847850/cross-platform-way-of-getting-temp-directory-in-python
            'filename': os.path.join(tempfile.gettempdir(), 'lmit.log')
        },
        'console': {
            'level': 'CRITICAL',
            'class': 'logging.StreamHandler',
            'formatter': 'free'
        }
    },
    'loggers': {
        'debug': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
        'verbose': {
            'handlers': ['file', 'console'],
            'level': 'INFO'
        },
        'standard': {
            'handlers': ['file'],
            'level': 'INFO'
        }
    }
}


def tempfile_name():
    """Return the tempfile name (full path)."""
    ret = os.path.join(tempfile.gettempdir(), 'lmit.log')
    if os.access(ret, os.F_OK) and not os.access(ret, os.W_OK):
        print("WARNING: Couldn't write to log file {0}: (Permission denied)".format(ret))
        ret = tempfile.mkstemp(prefix='lmit', suffix='.tmp', text=True)
        print("Create a new log file: {0}".format(ret[1]))
        return ret[1]

    return ret


def lmit_logger():
    """Build and return the logger."""
    temp_path = tempfile_name()
    _logger = logging.getLogger()
    LOGGING_CFG['handlers']['file']['filename'] = temp_path
    dictConfig(LOGGING_CFG)

    return _logger

logger = lmit_logger()

