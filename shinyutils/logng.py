"""logng.py: utilities for logging."""

import argparse
import logging

from rich.logging import RichHandler


def build_log_argp(base_parser):
    """Add an argument for logging to the base_parser."""

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


def conf_logging(args=None, log_level=None):
    """Configure logging using args from `build_log_argp`."""
    if log_level is None:
        if (
            args is not None
            and hasattr(args, "log_level")
            and args.log_level is not None
        ):
            log_level = args.log_level
        else:
            log_level = "INFO"
    log_level_i = getattr(logging, log_level, logging.INFO)

    logging.basicConfig(
        level=log_level_i,
        format="%(message)s",
        datefmt="[%X] ",
        handlers=[RichHandler()],
    )
    logging.root.setLevel(log_level_i)
