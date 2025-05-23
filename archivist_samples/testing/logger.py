"""Creates the root logger as a simple console streamer. Follows the Django-style
logging configuration where the logging system forms a hierarchy of loggers
all potentially independently configurable.

This model allows controlling loggers that are part of the dependency list. For
example setting a debug logging level will show debug output from the underlying
urllib3 package.

URL: https://docs.djangoproject.com/en/3.2/topics/logging/
"""

# pylint:  disable=missing-docstring

import logging
import logging.config

# root logger for all code
LOGGER = logging.getLogger()


def set_logger(level):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": level,
            },
        }
    )
