"""logng.py: utilities for logging."""

import logging

import crayons


def build_log_argp(base_parser):
    """Build a parser group for logging arguments."""
    log_parser = base_parser.add_argument_group("logging")
    log_parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
    )
    log_parser.add_argument("--log-file", type=str, default=None)
    return log_parser


class ColorfulLogRecord(logging.LogRecord):

    """LogRecord with colors."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.levelno == logging.CRITICAL:
            colf = crayons.red
        elif self.levelno == logging.ERROR:
            colf = crayons.magenta
        elif self.levelno == logging.WARNING:
            colf = crayons.yellow
        elif self.levelno == logging.INFO:
            colf = crayons.cyan
        else:
            colf = crayons.green
        self.levelname = str(colf(self.levelname, bold=True))

        self.msg = (
            crayons.colorama.Style.BRIGHT
            + str(self.msg)
            + crayons.colorama.Style.NORMAL
        )


def conf_logging(args=None, log_level=None, log_file=None):
    """Configure logging using args from `build_log_argp`."""
    if log_level is None:
        if args is not None and hasattr(args, "log_level"):
            log_level = args.log_level
        else:
            log_level = "INFO"
    log_level_i = getattr(logging, log_level, logging.INFO)

    if log_file is None and args is not None and hasattr(args, "log_file"):
        log_file = args.log_file

    logging.basicConfig(
        filename=log_file,
        level=log_level_i,
        format="%(levelname)s:%(filename)s.%(funcName)s.%(lineno)d:%(message)s",
    )
    if log_file is None:
        logging.setLogRecordFactory(ColorfulLogRecord)
