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
`ArgumentParser` type representing a list of `int` values. Accepts a string of comma separated values, e.g., `'1,2,3'`.

#### `InputFileType`
`FileType` restricted to input files, (with `'-'` for `stdin`). Returns a `file` object.

#### `OutputFileType`
`FileType` restricted to output files (with `'-'` for `stdout`). The file's parent directories are created if needed. Returns a `file` object.

#### `InputDirectoryType`
`ArgumentParser` type representing a directory. Returns a `Path` object.

#### `OutputDirectoryType`
`ArgumentParser` type representing an output directory. The directory is created if it doesn't exist. Returns a `Path` object.

#### `ClassType`
`ArgumentParser` type representing sub-classes of a given base class. The returned value is a `class`.
```python
class Base:
    pass

class A(Base):
    pass

class B(Base):
    pass

arg_parser.add_argument("--cls", type=ClassType(Base), default=A)
```

#### `KeyValuePairsType`
`ArgumentParser` type representing mappings. Accepts inputs of the form `str=val,[...]` where val is `int/float/str`. Returns a `dict`.

#### `shiny_arg_parser`
`ArgumentParser` object with `LazyHelpFormatter`, and arguments from sub-modules.

### `logng`
Utilities for logging.
#### `build_log_argp`
Creates an argument group with logging arguments.
```python
>>> arg_parser = ArgumentParser()
>>> _ = build_log_argp(arg_parser)  # returns the parser
>>> arg_parser.print_help()
usage: -c [-h] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

optional arguments:
  -h, --help            show this help message and exit
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
```
This function is called on `shiny_arg_parser` when `shinyutils` is imported.

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

#### `MatWrap`
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

Use `mw.configure` to configure plots. Arguments (defaults in bold) are:
* `context`: seaborn context (__paper__/poster/talk/notebook)
* `style`: seaborn style (white/whitegrid/dark/darkgrid/__ticks__)
* `font`: any font available to fontspec (default __Latin Modern Roman__)
* `latex_pkgs`: additional latex packages to be included before defaults
* `**rc_extra`: matplotlib rc parameters to override defaults
`mw.configure()` is called when `shinyutils.matwrap` is imported.

Use `add_parser_config_args` to add matwrap config options to an argument parser.
```python
>>> arg_parser = ArgumentParser()
>>> _ = mw.add_parser_config_args(arg_parser, group_title="plotting options")  # returns the parser group
>>> arg_parser.print_help()
usage: -c [-h] [--plotting-context {paper,notebook,talk,poster}]
          [--plotting-style {white,dark,whitegrid,darkgrid,ticks}]
          [--plotting-font PLOTTING_FONT]
          [--plotting-latex-pkgs PLOTTING_LATEX_PKGS [PLOTTING_LATEX_PKGS ...]]
          [--plotting-rc-extra PLOTTING_RC_EXTRA]

optional arguments:
  -h, --help            show this help message and exit

plotting options:
  --plotting-context {paper,notebook,talk,poster}
  --plotting-style {white,dark,whitegrid,darkgrid,ticks}
  --plotting-font PLOTTING_FONT
  --plotting-latex-pkgs PLOTTING_LATEX_PKGS [PLOTTING_LATEX_PKGS ...]
  --plotting-rc-extra PLOTTING_RC_EXTRA
```
`group_title` is optional, and if omitted, matwrap options will not be put in a separate group. When `shinyutils.matwrap` is imported, this function is called on `shiny_arg_parser`.

#### Plot
`Plot` is a wrapper around a single matplotlib plot, designed to be used as a context manager.
```python
from shinyutils.matwrap import Plot

with Plot(save_file, title, sizexy, labelxy, logxy) as ax:
  ...
```
Only the `save_file` argument is mandatory. When entering the context, `Plot` returns the plot axes, and when leaving, the plot is saved to the provided path.
