# shinyutils
Various utilities for common tasks. :sparkles: :sparkles: :sparkles:

## Setup
Install with `pip`.

```bash
pip install git+ssh://git@github.com/jayanthkoushik/shinyutils.git
```

## `matwrap`
Wrapper around `matplotlib` and `seaborn`.
### Usage
```python
from shinyutils import MatWrap as mw  # do not import `matplotlib`, `seaborn`

fig = mw.plt().figure()
ax = fig.add_subplot(111)  # `ax` can be used normally now

# Use class methods in `MatWrap` to access `matplotlib`/`seaborn` functions.
mw.mpl()  # returns `matplotlib` module
mw.plt()  # returns `matplotlib.pyplot` module
mw.sns()  # returns `seaborn` module

# Use `set_size_tight` to set size with a tight layout.
mw.set_size_tight(fig, (4, 3))
```

## `subcls`
Utility functions for dealing with subclasses.
### Functions
__`get_subclasses(cls)`__: returns a list of all the subclasses of `cls`.<br>
__`get_subclass_names(cls)`__: returns a list of names of all subclasses of `cls`.<br>
__`get_subclass_from_name(base_cls, cls_name)`__: return the subclass of `base_cls` named `cls_name`.<br>
__`build_subclass_object(base_cls, cls_name, kwargs)`__: return an instance of `get_subclass_from_name` initialized using `kwargs`.

## `argp`
Utilities for argument parsing.
### `LazyHelpFormatter`
`HelpFormatter` with sane defaults, and colors (courtesy of crayons)! To use, simply pass `formatter_class=LazyHelpFormatter` when creating `ArgumentParser` instances.

```python
arg_parser = ArgumentParser(formatter_class=LazyHelpFormatter)
sub_parsers = arg_parser.add_subparsers(dest="cmd")
sub_parsers.required = True
# `formatter_class` needs to be set for sub parsers as well.
cmd1_parser = sub_parsers.add_parser("cmd1", formatter_class=LazyHelpFormatter)
```

### `comma_separated_ints`
`ArgumentParser` type representing a comma separated list of ints (example `1,2,3,4`).
```python    
arg_parser.add_argument("--csi", type=comma_separated_ints)
```

## `logng`
Utilities for logging.
### `build_log_argp`
Creates an argument group with logging arguments.
```
>>> arg_parser = ArgumentParser()
>>> log_parser = build_log_argp(arg_parser)
>>> arg_parser.print_help()
usage: python [-h] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
            [--log-file LOG_FILE]

optional arguments:
-h, --help            show this help message and exit

logging:
--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
--log-file LOG_FILE
```

### `conf_logging`
Configure global logging (and add colors!) using arguments returned by `ArgumentParser.parse_args`. Both `log_level` and `log_file` can be over-ridden with keyword arguments to the function. Colors are not enabled if logging to a file.
```python
args = arg_parser.parse_args()
conf_logging(args)
conf_logging(args, log_level="INFO")  # override `log_level`
conf_logging(log_level="ERROR", log_file="log.out")  # `args` is also optional
logging.info("this won't be logged")
```
