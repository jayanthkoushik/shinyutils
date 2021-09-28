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


__all__ = ["build_log_argp", "conf_logging"]


def build_log_argp(base_parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add a `--log-level` parser argument to set the log level.

    Args:
        base_parser: `ArgumentParser` instance to add the argument to. The same instance
            is returned from the function.

    Example::

        >>> arg_parser = ArgumentParser(
                add_help=False, formatter_class=corgy.CorgyHelpFormatter
        )
        >>> build_log_argp(arg_parser)
        >>> arg_parser.print_help()
        options:
          --log-level str  ({'DEBUG'/'INFO'/'WARNING'/'ERROR'/'CRITICAL'} optional)
    """

    class _SetLogLevel(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            conf_logging(log_level=values)
            setattr(namespace, self.dest, values)

    base_parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        action=_SetLogLevel,
    )
    return base_parser


def conf_logging(log_level: str = "INFO", use_colors: Optional[bool] = None):
    """Configure the root logging handler.

    Args:
        log_level: A string log level (`DEBUG`/[`INFO`]/`WARNING`/`ERROR`/`CRITICAL`).
        use_colors: Whether to use colors from `rich.logging`. Default is to use
            colors if `rich` is installed.
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
            raise ImportError(
                f"{RICH_IMPORT_ERROR}: disable colors or install shinyutils[color]"
            )

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
        logging.info("for logging color support install shinyutils[color]")


conf_logging()
