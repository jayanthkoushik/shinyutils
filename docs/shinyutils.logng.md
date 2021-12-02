# shinyutils.logng module

Utilities for logging.


### shinyutils.logng.conf_logging(log_level='INFO', use_colors=None, arg_parser=None, arg_name='--log-level', arg_help='set the log level')
Set up logging.

This function configures the root logger, and optionally, adds an argument to an
`ArgumentParser` instance for setting the log level from the command line.


* **Parameters**


    * **log_level** – A string log level (`DEBUG`/`INFO`/`WARNING`/`ERROR`/`CRITICAL`).
    The default is `INFO`.


    * **use_colors** – Whether to use colors from `rich.logging`. Default is to use
    colors if `rich` is installed.


    * **arg_parser** – An `ArgumentParser` instance to add a log level argument to. If
    `None` (the default), no argument is added. The added argument will update
    the log level when parsed from the command line.


    * **arg_name** – The name of the argument added to `arg_parser`. The default is
    `--log-level`.


    * **arg_help** – The help string for the argument added to `arg_parser`. The default
    is “set the log level”.


Usage:

```python
conf_logging("DEBUG")
conf_logging("INFO", use_colors=False)  # force no colors

parser = ArgumentParser()
conf_logging(log_level="DEBUG", arg_parser=parser)  # add argument to parser
parser.parse_args(["--log-level", "INFO"])  # update log level to INFO
```
