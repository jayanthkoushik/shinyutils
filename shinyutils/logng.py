"""Utilities for logging."""

import argparse
import logging
import os
from typing import Literal, Optional

try:
    from rich.logging import RichHandler
except ImportError:
    HAS_RICH = False
else:
    HAS_RICH = True


__all__ = ("conf_logging", "is_debug_mode")


class _SetLogLevel(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        logging.root.setLevel(values)
        setattr(namespace, self.dest, values)


def conf_logging(
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
    use_colors: Optional[bool] = None,
    arg_parser: Optional[argparse.ArgumentParser] = None,
    arg_name: str = "--log-level",
    arg_help: str = "set the log level",
    use_env_var: bool = True,
    fail_on_bad_env_var: bool = False,
):
    """Set up logging.

    This function configures the root logger, and optionally, adds an argument to an
    `ArgumentParser` instance for setting the log level from the command line.

    Args:
        log_level: A string log level (`DEBUG`/`INFO`/`WARNING`/`ERROR`/`CRITICAL`).
            The default is `INFO`.
        use_colors: Whether to use colors from `rich.logging`. Default is to use
            colors if `rich` is installed.
        arg_parser: An `ArgumentParser` instance to add a log level argument to. If
            `None` (the default), no argument is added. The added argument will update
            the log level when parsed from the command line.
        arg_name: The name of the argument added to `arg_parser`. The default is
            `--log-level`.
        arg_help: The help string for the argument added to `arg_parser`. The default
            is "set the log level".
        use_env_var: Whether to read the log level from an environment variable named
            `LOG_LEVEL` (True by default). The value of the variable should be a string
            log level (case insensitive).
        fail_on_bad_env_var: Whether to raise an exception if the environment variable
            is set to an invalid log level (False by default).

    Usage::

        conf_logging("DEBUG")
        conf_logging("INFO", use_colors=False)  # force no colors

        parser = ArgumentParser()
        conf_logging(log_level="DEBUG", arg_parser=parser)  # add argument to parser
        parser.parse_args(["--log-level", "INFO"])  # update log level to INFO

    The order of precedence for the log level is (highest to lowest): 1) command line
    argument, 2) environment variable, 3) this function's argument.
    """
    if use_env_var and (_env_log_level := os.getenv("LOG_LEVEL", None)) is not None:
        if _env_log_level.upper() not in (
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ):
            if fail_on_bad_env_var:
                raise ValueError(
                    f"invalid log level from environment variable: {_env_log_level}"
                )
        else:
            log_level = _env_log_level.upper()  # type: ignore
    logging.root.setLevel(log_level)

    if use_colors is None:
        use_colors = HAS_RICH
    elif use_colors is True:
        if not HAS_RICH:
            raise ImportError("cannot enable colored logging: could not import `rich`")
    inform_about_color = not HAS_RICH

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

    if arg_parser is not None:
        arg_parser.add_argument(
            arg_name,
            type=str,
            choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
            action=_SetLogLevel,
            help=arg_help,
            default=log_level,
        )


def is_debug_mode() -> bool:
    """Return whether the current log level is `DEBUG`."""
    return logging.root.level == logging.DEBUG
