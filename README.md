# shinyutils
Various utilities for common tasks. :sparkles: :sparkles: :sparkles:

## Setup
Install with `pip`. Additional features can be enabled with the `[<feature>]` syntax shown below. Available optional features are:
* `color`: color support for logging and argument parsing
* `plotting`: support for `matplotlib` and `seaborn`
```bash
pip install shinyutils  # basic install
pip install "shinyutils[color]"  # install with color support
pip install "shinyutils[color,plotting]"  # install with color and plotting support
pip install "shinyutils[all]"  # install with all optional features
```

## Components

### `subcls`
Utility functions for dealing with subclasses.

#### Functions
* __`get_subclasses(cls)`__: returns a list of all the subclasses of `cls`.
* __`get_subclass_names(cls)`__: returns a list of names of all subclasses of `cls`.
* __`get_subclass_from_name(base_cls, cls_name)`__: return the subclass of `base_cls` named `cls_name`.

### `argp`
Utilities for argument parsing.

#### `LazyHelpFormatter`
`HelpFormatter` with sane defaults, and colors (courtesy of `crayons`)! To use, simply pass `formatter_class=LazyHelpFormatter` when creating `ArgumentParser` instances.
```python
arg_parser = ArgumentParser(formatter_class=LazyHelpFormatter)
sub_parsers = arg_parser.add_subparsers(dest="cmd")
sub_parsers.required = True
# `formatter_class` needs to be set for sub parsers as well.
cmd1_parser = sub_parsers.add_parser("cmd1", formatter_class=LazyHelpFormatter)
```

#### `CommaSeparatedInts`
`ArgumentParser` type representing a comma separated list of ints (example `1,2,3,4`).
```python
arg_parser.add_argument("--csi", type=CommaSeparatedInts())
```

#### `OutputFileType`
`ArgumentParser` type representing an output file. The file's base directory is created if needed. The returned value is a file object.

#### `OutputDirectoryType`
`ArgumentParser` type representing an output directory. The directory is created if it doesn't exist.

#### `ClassType`
`ArgumentParser` type representing sub-classes of a given base class. The returned value is a class.
```python
class Base:
    pass

class A(Base):
    pass

class B(Base):
    pass

arg_parser.add_argument("--cls", type=ClassType(Base), default=A)
```

#### `shiny_arg_parser`
`ArgumentParser` object with LazyHelpFormatter, and logging argument.

### `logng`
Utilities for logging.
#### `build_log_argp`
Creates an argument group with logging arguments.
```
>>> arg_parser = ArgumentParser()
>>> build_log_argp(arg_parser)
>>> arg_parser.print_help()
usage: test.py [-h] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

optional arguments:
  -h, --help            show this help message and exit
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
```

#### `conf_logging`
Configures global logging using arguments returned by `ArgumentParser.parse_args`. `log_level` can be over-ridden with the keyword argument. Colors (enabled by default if `rich` is installed) can be toggled.
```python
args = arg_parser.parse_args()
conf_logging(args)
conf_logging(args, log_level="INFO")  # override `log_level`
conf_logging(use_colors=False)  # disable colors
```
When imported, `shinyutils` calls `conf_logging` without any arguments.

### `matwrap`
Wrapper around `matplotlib` and `seaborn`.

#### Usage
```python
from shinyutils.matwrap import MatWrap as mw  # do not import `matplotlib`, `seaborn`

mw.configure()  # this should be called before importing any packages that import matplotlib

fig = mw.plt().figure()
ax = fig.add_subplot(111)  # `ax` can be used normally now

# Use class methods in `MatWrap` to access `matplotlib`/`seaborn` functions.
mw.mpl()  # returns `matplotlib` module
mw.plt()  # returns `matplotlib.pyplot` module
mw.sns()  # returns `seaborn` module
```

#### Configuration
Use `mw.configure` to configure plots. Arguments (defaults in bold) are:
* `context`: seaborn context (__paper__/poster/talk/notebook)
* `style`: seaborn style (white/whitegrid/dark/darkgrid/__ticks__)
* `font`: any font available to fontspec (default __Latin Modern Roman__)
* `latex_pkgs`: additional latex packages to be included before defaults
* `**rc_extra`: matplotlib rc parameters to override defaults
```
