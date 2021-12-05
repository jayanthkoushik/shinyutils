# shinyutils.matwrap module

Utilities for matplotlib and seaborn.

`MatWrap.configure` is called upon importing this module, which enables default config.


### _class_ shinyutils.matwrap.MatWrap()
Wrapper for `matplotlib`, `matplotlib.pyplot`, and `seaborn`.

Usage:

```python
# Do not import `matplotlib` or `seaborn`.
from shinyutils.matwrap import MatWrap as mw
# Configure with `mw.configure` (refer to `configure` docs for details).
mw.configure()

fig = mw.plt().figure()
ax = fig.add_subplot(111)  # `ax` can be used normally now

# Use class properties in `MatWrap` to access `matplotlib`/`seaborn` functions.
mw.mpl  # returns `matplotlib` module
mw.plt  # returns `matplotlib.pyplot` module
mw.sns  # returns `seaborn` module

# You can also import the module names from `matwrap`
from shinyutils.matwrap import mpl, plt, sns

fig = plt.figure()
...
```


#### _classmethod_ configure(context='paper', style='ticks', font='Latin Modern Roman', latex_pkgs=None, backend=None, \*\*rc_extra)
Configure matplotlib and seaborn.


* **Parameters**


    * **context** – Seaborn context ([`paper`]/`poster`/`notebook`).


    * **style** – Seaborn style (`darkgrid`/`whitegrid`/`dark`/`white`/[`ticks`]).


    * **font** – Font, passed directly to fontspec (default: `Latin Modern Roman`).


    * **latex_pkgs** – List of packages to load in latex pgf preamble.


    * **backend** – Matplotlib backend to override default (pgf).


    * **rc_extra** – Matplotlib params (will overwrite defaults).



#### _class property_ mpl()
`matplotlib` module.


#### _class property_ plt()
`matplotlib.pyplot` module.


#### _class property_ sns()
`seaborn` module.


#### _classmethod_ palette(n=8)
Color universal design palette.


### _class_ shinyutils.matwrap.PlottingArgs(\*\*kwargs)
Plotting arguments that can be added to `ArgumentParser` instances.

`MatWrap.configure` is called with the chosen arguments when an instance of this
class is created.

Usage:

```python
>>> arg_parser = ArgumentParser(add_help=False, formatter_class=Corgy)
>>> PlottingArgs.add_to_parser(arg_parser, name_prefix="plotting")
>>> arg_parser.print_help()
options:
    --plotting-context str
        seaborn plotting context ({'paper'/'notebook'/'talk'/'poster'}
        default: 'paper')
    --plotting-style str
        seaborn plotting style
        ({'white'/'dark'/'whitegrid'/'darkgrid'/'ticks'} default: 'ticks')
    --plotting-font str
        font for plots (default: 'Latin Modern Roman')
    --plotting-backend str
        matplotlib backend (default: 'pgf')
```

The class can also be used to create an argument group inside another `Corgy`
class:

```python
class A(Corgy):
    plotting: Annotated[PlottingArgs, "plotting arguments"]
```


#### _property_ context()
seaborn plotting context


#### _property_ style()
seaborn plotting style


#### _property_ font()
font for plots


#### _property_ backend()
matplotlib backend


### _class_ shinyutils.matwrap.Plot(save_file=None, title=None, sizexy=None, labelxy=(None, None), logxy=(False, False))
Wrapper around a single matplotlib plot.

This class is a context manager that returns a matplotlib `axis` instance when
entering the context. The plot is closed, and optionally, saved to a file when
exiting the context.


* **Parameters**


    * **save_file** – Path to save plot to. If `None` (the default), the plot is not
    saved.


    * **title** – Optional title for plot.


    * **sizexy** – Size tuple (width, height) in inches. If `None` (the default), the
    plot size will be determined automatically by matplotlib.


    * **labelxy** – Tuple of labels for the x and y axes respectively. If either value is
    `None` (the default), the corresponding axis will not be labeled.


    * **logxy** – Tuple of booleans indicating whether to use a log scale for the x and y
    axis respectively (default: `(False, False)`).


Usage:

```python
with Plot() as ax:
    # Use `ax` to plot stuff.
    ...
```
