# shinyutils.logng module

Utilities for logging.


### shinyutils.logng.conf_logging(log_level='INFO', use_colors=None, arg_parser=None, arg_name='--log-level', arg_help='set the log level', use_env_var=True, fail_on_bad_env_var=False)
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


    * **use_env_var** – Whether to read the log level from an environment variable named
    `LOG_LEVEL` (True by default). The value of the variable should be a string
    log level (case insensitive).


    * **fail_on_bad_env_var** – Whether to raise an exception if the environment variable
    is set to an invalid log level (False by default).


Usage:

```python
conf_logging("DEBUG")
conf_logging("INFO", use_colors=False)  # force no colors

parser = ArgumentParser()
conf_logging(log_level="DEBUG", arg_parser=parser)  # add argument to parser
parser.parse_args(["--log-level", "INFO"])  # update log level to INFO
```

The order of precedence for the log level is (highest to lowest): 1) command line
argument, 2) environment variable, 3) this function’s argument.


### shinyutils.logng.is_debug_mode()
Return whether the current log level is `DEBUG`.
