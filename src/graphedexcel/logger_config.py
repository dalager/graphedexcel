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
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "simple",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": "app.log",
            "encoding": "utf8",
            "mode": "w",  # 'a' for append, 'w' for overwrite
        },  # You can add more handlers (e.g., FileHandler) here
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        # Define loggers for specific modules if needed
    },
}

logging.config.dictConfig(logging_config)
