"""Utilities for logging.

`conf_logging` is called upon importing this module, which sets the log level to
`INFO`, and enables colored logging if `rich` is installed.
"""

import argparse
import logging
from typing import Optional

try:
    from rich.logging import RichHandler
except ImportError as e:
    HAS_RICH = False
    RICH_IMPORT_ERROR = e
else:
    HAS_RICH = True


__all__ = ("conf_logging",)


class _SetLogLevel(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        conf_logging(log_level=values)
        setattr(namespace, self.dest, values)


def conf_logging(*, log_level: str = "INFO", use_colors: Optional[bool] = None):
    """Configure the root logging handler.

    Args:
        log_level: A string log level (`DEBUG`/[`INFO`]/`WARNING`/`ERROR`/`CRITICAL`).
        use_colors: Whether to use colors from `rich.logging`. Default is to use
            colors if `rich` is installed.

    Note that this function only accepts keyword arguments.
    """
    log_level_i = getattr(logging, log_level, logging.INFO)
    logging.root.setLevel(log_level_i)

    inform_about_color = False

    if use_colors is None:
        use_colors = HAS_RICH
        if not HAS_RICH:
            inform_about_color = True

    elif use_colors is True:
        if not HAS_RICH:
            raise ImportError(f"{RICH_IMPORT_ERROR}: disable colors or install `rich`")

    # Remove existing root handlers
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)

    # Create root handler
    root_handler: logging.Handler
    if use_colors:
        root_handler = RichHandler()
        fmt = "%(message)s"
        datefmt = "[%X] "
    else:
        root_handler = logging.StreamHandler()
        fmt = "%(asctime)s %(levelname)-10s %(filename)s:%(lineno)d: %(message)s"
        datefmt = "[%X]"

    # Create formatter and add handler to root logger
    fmter = logging.Formatter(fmt, datefmt)
    root_handler.setFormatter(fmter)
    logging.root.addHandler(root_handler)

    if inform_about_color:
        logging.info("for logging color support install `rich`")


conf_logging()
