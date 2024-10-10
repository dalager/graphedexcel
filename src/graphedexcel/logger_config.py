# logger_config.py

import logging
import logging.config

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,  # Preserve other loggers
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "simple": {
            "format": "%(levelname)s: %(message)s",
        },
        "minimal": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "simple",
            "class": "logging.StreamHandler",
        },
        "minimalconsole": {
            "level": "INFO",
            "formatter": "minimal",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": "app.log",
            "encoding": "utf8",
            "mode": "w",  # 'a' for append, 'w' for overwrite
        },
    },
    "loggers": {
        "graphedexcel": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {"handlers": ["minimalconsole"], "level": "WARNING"},
}

logging.config.dictConfig(logging_config)
