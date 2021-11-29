# shinyutils package

Collection of personal utilities.

## Submodules

## shinyutils.logng module

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

## shinyutils.matwrap module

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


### _class_ shinyutils.matwrap.PlottingArgs(\*\*args)
Plotting arguments that can be added to `ArgumentParser` instances.

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

## shinyutils.pt module

Utilities for pytorch.


### _class_ shinyutils.pt.PTOpt(\*\*kwargs)
Wrapper around PyTorch optimizer and learning rate scheduler.

Usage:

```python
>>> opt = PTOpt(Adam, {"lr": 0.001})
>>> net = nn.Module(...)  # some network
>>> opt.set_weights(net.parameters())
>>> opt.zero_grad()
>>> opt.step()
```


#### _property_ optim_cls()
optimizer class


#### _property_ optim_params()
arguments for the optimizer


#### _property_ lr_sched_cls()
learning rate scheduler class


#### _property_ lr_sched_params()
arguments for the learning rate scheduler


#### set_weights(weights)
Set weights of underlying optimizer.


#### zero_grad()
Call `zero_grad` on underlying optimizer.


#### step()
Call `step` on underlying optimizer, and lr scheduler (if present).


#### _static_ add_help_args_to_parser(base_parser, group_title='pytorch help')
Add parser arguments for help on PyTorch optimizers and lr schedulers.

Example:

```python
>>> arg_parser = ArgumentParser(
        add_help=False, formatter_class=corgy.CorgyHelpFormatter
)
>>> PTOpt.add_help(arg_parser)
>>> arg_parser.print_help()
pytorch help:
  --explain-optimizer cls  describe arguments of a torch optimizer
                           (optional)
  --explain-lr-sched cls   describe arguments of a torch lr scheduler
                           (optional)
>>> arg_parser.parse_args(["--explain-optimizer", "Adamax"])
Adamax(params, lr=0.002, betas=(0.9, 0.999), eps=1e-08, weight_decay=0)
```


### _class_ shinyutils.pt.FCNet(\*args, \*\*kwargs)
Fully connected network.


#### _property_ in_dim()
number of input features


#### _property_ out_dim()
number of output features


#### _property_ hidden_dims()
hidden layer dimensions


#### _property_ hidden_act()
activation function for hidden layers


#### _property_ out_act()
activation function for output layer


#### forward(x)
Forward a tensor through the network, and return the result.


* **Parameters**

    **x** – Input tensor of shape `(batch_size, in_dim)`.



### _class_ shinyutils.pt.NNTrainer(\*\*args)
Helper class for training a model on a dataset.


#### _property_ train_iters()
number of training iterations


#### _property_ ptopt()
optimizer


#### _property_ batch_size()
batch size for training


#### _property_ data_load_workers()
number of workers for loading data


#### _property_ shuffle()
whether to shuffle the dataset


#### _property_ pin_memory()
whether to pin data to CUDA memory


#### _property_ drop_last()
whether to drop the last incomplete batch


#### _property_ pbar_desc()
description for training progress bar


#### set_dataset(value)
Set the training data.


* **Parameters**

    **value** – `torch.utils.data.Dataset` instance, or tuple of `torch.Tensor` or
    `np.ndarray` objects.



#### train(model, loss_fn, post_iter_hook=None)
Train a model.


* **Parameters**


    * **model** – Model (`nn.Module` instance) to train.


    * **loss_fn** – Loss function mapping input tensors to a loss tensor.


    * **post_iter_hook** – Optional callback function to call after each iteration.
    The function will be called with arguments
    `(iteration, x_batch, y_batch, yhat_batch, loss)`.



### _class_ shinyutils.pt.TBLogs(path=None)
TensorBoard logs type.


* **Parameters**

    **path** – Path to log directory. If `None` (default), a mock instance is
    returned.


Usage:

```python
tb_logs = TBLogs("tmp/tb")
tb_logs.writer  # `SummaryWriter` instance
TBLogs.mock  # mock instance
```


#### _class property_ mock()
Mock instace that no-ops for every call.

## shinyutils.sh module

Stateful wrapper to execute shell commands.


### _class_ shinyutils.sh.SH(shell=('sh', '-i'), loop=None)
Wrapper around an interactive shell process.

This class can be used to execute multiple shell commands within a single shell
session; shell output (stdout and stderr) is captured and returned as a string.
The class must be used as a context manager; both synchronous and asynchronous
modes are supported.


* **Parameters**


    * **shell** – The shell command to execute, as a sequence of strings. This must start
    an interactive shell, and defaults to `sh -i`.


    * **loop** – Optional event loop to use. If not provided, the default event loop is
    used instead.


Usage:

```python
# synchronous mode
with SH() as sh:
    sh("x=1")
    print(sh("echo $x"))

# asynchronous mode
async with SH() as sh:
    await sh("x=1")
    print(await sh("echo $x"))
```

**NOTE**: The class uses a custom prompt string to identify the end of a command. So,
do not run any commands that change the prompt. Similarly, background jobs are
not supported, if they produce any output. The behavior in these cases is
undefined.
