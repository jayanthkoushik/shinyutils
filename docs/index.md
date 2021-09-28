# shinyutils package

Collection of personal utilities.

## Submodules

## shinyutils.logng module

Utilities for logging.

`conf_logging` is called upon importing this module, which sets the log level to
`INFO`, and enables colored logging if `rich` is installed.


### shinyutils.logng.build_log_argp(base_parser: argparse.ArgumentParser)
Add a `--log-level` parser argument to set the log level.


* **Parameters**

    **base_parser** – `ArgumentParser` instance to add the argument to. The same instance
    is returned from the function.


Example:

```python
>>> arg_parser = ArgumentParser(
        add_help=False, formatter_class=corgy.CorgyHelpFormatter
)
>>> build_log_argp(arg_parser)
>>> arg_parser.print_help()
options:
  --log-level str  ({'DEBUG'/'INFO'/'WARNING'/'ERROR'/'CRITICAL'} optional)
```


### shinyutils.logng.conf_logging(log_level: str = 'INFO', use_colors: Optional[bool] = None)
Configure the root logging handler.


* **Parameters**

    
    * **log_level** – A string log level (`DEBUG`/[`INFO`]/`WARNING`/`ERROR`/`CRITICAL`).


    * **use_colors** – Whether to use colors from `rich.logging`. Default is to use
    colors if `rich` is installed.


## shinyutils.matwrap module

Utilities for matplotlib and seaborn.


### _class_ shinyutils.matwrap.MatWrap()
Wrapper for `matplotlib`, `matplotlib.pyplot`, and `seaborn`.

Usage:

```python
# Do not import `matplotlib` or `seaborn`.
from shinyutils.matwrap import MatWrap as mw
# Call before importing any packages that import matplotlib.
mw.configure()

fig = mw.plt().figure()
ax = fig.add_subplot(111)  # `ax` can be used normally now

# Use class methods in `MatWrap` to access `matplotlib`/`seaborn` functions.
mw.mpl()  # returns `matplotlib` module
mw.plt()  # returns `matplotlib.pyplot` module
mw.sns()  # returns `seaborn` module
```


#### _classmethod_ configure(context: str = 'paper', style: str = 'ticks', font: str = 'Latin Modern Roman', latex_pkgs: Optional[List[str]] = None, \*\*rc_extra)
Configure matplotlib and seaborn.


* **Parameters**

    
    * **context** – Seaborn context ([`paper`]/`poster`/`notebook`).


    * **style** – Seaborn style (`darkgrid`/`whitegrid`/`dark`/`white`/[`ticks`]).


    * **font** – Font, passed directly to fontspec (default: `Latin Modern Roman`).


    * **latex_pkgs** – List of packages to load in latex pgf preamble.


    * **rc_extra** – Matplotlib params (will overwrite defaults).



#### _classmethod_ mpl()
`matplotlib` module.


#### _classmethod_ plt()
`matplotlib.pyplot` module.


#### _classmethod_ sns()
`seaborn` module.


#### _classmethod_ palette()
Color-blindness friendly palette of 8 colors in hex.


#### _static_ set_size_tight(fig, size: Tuple[int, int])
Set the size of a matplotlib figure.


* **Parameters**

    
    * **fig** – Matplotlib `Figure` instance.


    * **size** – Tuple (width, height) in inches.



#### _static_ add_parser_config_args(base_parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup], group_title: Optional[str] = 'plotting options')
Add arguments for configuring plotting to a parser.


* **Parameters**

    
    * **base_parser** – Argument parser or group to add arguments to.


    * **group_title** – Title to use for added options. If `None`, arguments will be
    added to the base parser. Otherwise, options will be added to a group
    with the given title. A new group will be created if `base_parser` is
    not a group.


Example:

```python
>>> arg_parser = ArgumentParser(
        add_help=False, formatter_class=corgy.CorgyHelpFormatter
    )
>>> MatWrap.add_parser_config_args(arg_parser)
>>> arg_parser.print_help()
plotting options:
  --plotting-context str
      ({'paper'/'notebook'/'talk'/'poster'} default: 'paper')
  --plotting-style str
      ({'white'/'dark'/'whitegrid'/'darkgrid'/'ticks'} default: 'ticks')
  --plotting-font str
      (default: 'Latin Modern Roman')
  --plotting-latex-pkgs [str [str ...]]
      (default: [])
  --plotting-rc-extra [key=val [key=val ...]]
      (default: [])
```


### _class_ shinyutils.matwrap.Plot(save_file: Optional[str] = None, title: Optional[str] = None, sizexy: Optional[Tuple[int, int]] = None, labelxy: Tuple[Optional[str], Optional[str]] = (None, None), logxy: Tuple[bool, bool] = (False, False))
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


### _class_ shinyutils.pt.PTOpt(weights: Iterable[torch.Tensor], optim_cls: Type[torch.optim.optimizer.Optimizer], optim_params: Mapping[str, Any], lr_sched_cls: Optional[Type[torch.optim.lr_scheduler._LRScheduler]] = None, lr_sched_params: Optional[Mapping[str, Any]] = None)
Wrapper around pytorch optimizer and learning rate scheduler.


* **Parameters**

    
    * **weights** – Iterable of `Tensor` weights to optimize.


    * **optim_cls** – `Optimizer` class to use.


    * **optim_params** – Mapping of parameters to pass to `optim_cls`.


    * **lr_sched_cls** – `LRScheduler` class to use for scheduling the learning rate.


    * **lr_sched_params** – Mapping of parameters to pass to `lr_sched_cls`.



#### zero_grad()
Call `zero_grad` on underlying optimizer.


#### step()
Call `step` on underlying optimizer and lr scheduler (if present).


#### _classmethod_ from_args(weights: Iterable[torch.Tensor], args: argparse.Namespace, arg_prefix: str = '')
Create `PTOpt` instance from a namespace of arguments.


* **Parameters**

    
    * **weights** – Iterable of `torch.Tensor` weights to optimize.


    * **args** – Namespace of arguments (argument names are as added by
    `add_parser_args`).


    * **arg_prefix** – Prefix for argument names (default: `""`).



#### _static_ add_parser_args(base_parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup], arg_prefix: str = '', group_title: Optional[str] = None, default_optim_cls: Optional[Type[torch.optim.optimizer.Optimizer]] = <class 'torch.optim.adam.Adam'>, default_optim_params: Optional[Mapping[str, Any]] = None, add_lr_decay: bool = True)
Add options to the base parser for pytorch optimizer and lr scheduling.


* **Parameters**

    
    * **base_parser** – Argument parser or group to add arguments to.


    * **arg_prefix** – Prefix for argument names (default: empty string).


    * **group_title** – Title to use for added options. If `None`, arguments will be
    added to the base parser. Otherwise, options will be added to a group
    with the given title. A new group will be created if `base_parser` is
    not a group.


    * **default_optim_cls** – Default `Optimizer` class (default: `Adam`).


    * **default_optim_params** – Default set of parameters to pass to the optimizer
    (default: `None`).


    * **add_lr_decay** – Whether to add options for lr decay (default: `True`).


Example:

```python
>>> arg_parser = ArgumentParser(
        add_help=False, formatter_class=corgy.CorgyHelpFormatter
)
>>> PTOpt.add_parser_args(arg_parser)
>>> arg_parser.print_help()
options:
  --optim-cls cls
      ({'Adadelta'/'Adagrad'/'Adam'/'AdamW'/'SparseAdam'/'Adamax'/'ASGD'
      /'SGD'/'Rprop'/'RMSprop'/'LBFGS'/'Adam'/'AdamW'/'SGD'/'RMSprop'/'R
      prop'/'ASGD'/'Adamax'/'Adadelta'} default: <class
      'torch.optim.adam.Adam'>)
  --optim-params [key=val [key=val ...]]
      (default: [])
  --lr-sched-cls cls
      ({'LambdaLR'/'MultiplicativeLR'/'StepLR'/'MultiStepLR'/'Exponentia
      lLR'/'CosineAnnealingLR'/'CyclicLR'/'CosineAnnealingWarmRestarts'/
      'OneCycleLR'/'SWALR'} optional)
  --lr-sched-params [key=val [key=val ...]]
      (default: [])
```


#### _static_ add_help(base_parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup], group_title: Optional[str] = 'pytorch help')
Add parser arguments for help on PyTorch optimizers and lr schedulers.


* **Parameters**

    
    * **base_parser** – `ArgumentParser` or `ArgumentGroup` to add options to.


    * **group_title** – Title for the group of options (default: `pytorch help`).
    If `group_title` is `None`, the options are added to the base parser,
    otherwise they are added to a group (a new one is created if
    `base_parser` is not a group).


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


### _class_ shinyutils.pt.FCNet(in_dim: int, out_dim: int, hidden_sizes: List[int], hidden_act: Callable[[torch.Tensor], torch.Tensor] = <function relu>, out_act: Optional[Callable[[torch.Tensor], torch.Tensor]] = None)
Template for a fully connected network.


* **Parameters**

    
    * **in_dim** – Number of input features.


    * **out_dim** – Number of output features.


    * **hidden_sizes** – List of hidden layer sizes.


    * **hidden_act** – Activation function for hidden layers (default: `relu`).


    * **out_act** – Activation function for output layer (default: `None`).



#### forward(x: torch.Tensor)
Propagate input tensor through the network.


#### _classmethod_ from_args(args: argparse.Namespace, arg_prefix: str = '')
Create `FCNet` instance from a namespace of arguments.


* **Parameters**

    
    * **args** – Namespace of arguments, with names as added by `add_parser_args`.


    * **arg_prefix** – Prefix for argument names (default: `""`).



#### _static_ add_parser_args(base_parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup], arg_prefix: str = '', group_title: Optional[str] = None, default_indim: Optional[int] = None, default_outdim: Optional[int] = None, default_hidden_sizes: Optional[int] = None, default_hidden_act: Optional[Callable[[torch.Tensor], torch.Tensor]] = <function relu>, default_out_act: Optional[Callable[[torch.Tensor], torch.Tensor]] = None)
Add options to a parser for building a `FCNet` object.


* **Parameters**

    
    * **base_parser** – `ArgumentParser` or `ArgumentGroup` to add options to.


    * **arg_prefix** – Prefix for argument names (default: `""`).


    * **group_title** – Title for the group of options If `None` (the default),
    the options are added to the base parser. Otherwise they are added
    to a group with the given title (a new one is created if `base_parser`
    is not a group).


    * **default_indim** – Default value for `indim` (default: `None`).


    * **default_outdim** – Default value for `outdim` (default: `None`).


    * **default_hidden_sizes** – Default value for `hidden_sizes` (default: `None`).


    * **default_hidden_act** – Default value for hidden activation (default: `relu`).


    * **default_out_act** – Default value for output activation (default: `None`).


Example:

```python
>>> arg_parser = ArgumentParser(
        add_help=False, formatter_class=corgy.CorgyHelpFormatter)
)
>>> FCNet.add_parser_args(arg_parser)
>>> arg_parser.print_help()
options:
  --fcnet-indim int
      (required)
  --fcnet-outdim int
      (required)
  --fcnet-hidden-sizes int [int ...]
      (required)
  --fcnet-hidden-act func
      (default: <function relu at 0x7faf08f86830>)
  --fcnet-out-act func
      (optional)
```


### _class_ shinyutils.pt.NNTrainer(batch_size: int, data_load_workers: int = 0, shuffle: bool = True, pin_memory: bool = True, drop_last: bool = True, device: torch.device = device(type='cpu'))
Helper class for training a model on a dataset.


* **Parameters**

    
    * **batch_size** – Batch size for training.


    * **data_load_workers** – Number of workers for loading data (default: `0`).


    * **shuffle** – Whether to shuffle the data (default: `True`).


    * **pin_memory** – When to pin data to CUDA memory (default: `True`).


    * **drop_last** – Whether to drop the last incomplete batch (default: `True`).


    * **device** – Device to use for training (default: `cuda` if available, else `cpu`).



#### set_dataset(value: torch.utils.data.dataset.Dataset)

#### set_dataset(value: Tuple[torch.Tensor, ...])

#### set_dataset(value: Tuple[numpy.ndarray, ...])
Set the training data.


* **Parameters**

    **value** – `torch.utils.data.Dataset` instance, or tuple of `torch.Tensor` or
    `np.ndarray` objects.



#### train(model: torch.nn.modules.module.Module, opt: shinyutils.pt.PTOpt, loss_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor], iters: int, pbar_desc: str = 'Training')
Train a model.


* **Parameters**

    
    * **model** – Model (`nn.Module` instance) to train.


    * **opt** – `PTOpt` instance to use for optimizing.


    * **loss_fn** – Loss function mapping input tensors to a loss tensor.


    * **iters** – Number of iterations to train for.


    * **pbar_desc** – Description for progress bar (default: `Training`).



### _class_ shinyutils.pt.SetTBWriterAction(option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None)
`argparse.Action` to set the `tb_writer` attribute.

The attribute (configurable via `SetTBWriterAction.attr`) is set to a
`SummaryWriter`, or a `Mock` of the class (if called without any value).

Usage:

```python
arg_parser = ArgumentParser()
arg_parser.add_argument(
    "--tb-dir",
    type=str,
    action=SetTBWriterAction,
)
arg_parser.set_defaults(tb_writer=Mock(SummaryWriter))
args = arg_parser.parse_args(["--tb-dir", "tmp/tb"])
args.tb_writer  # `SummaryWriter` instance
```
