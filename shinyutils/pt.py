"""Utilities for pytorch."""

try:
    import torch
except ImportError as e:
    e.msg += ": install shinyutils[pytorch]"  # type: ignore
    raise e

import inspect
import logging
from argparse import (
    _ArgumentGroup,
    Action,
    ArgumentParser,
    ArgumentTypeError,
    Namespace,
)
from typing import (
    Any,
    Callable,
    Iterable,
    List,
    Mapping,
    Optional,
    overload,
    Tuple,
    Type,
    Union,
)
from unittest.mock import Mock

import numpy as np
import torch.nn.functional as F
from corgy.types import KeyValueType, SubClassType
from torch import nn
from torch.optim import Adam
from torch.optim.lr_scheduler import _LRScheduler
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader, Dataset, TensorDataset
from tqdm import trange

try:
    from torch.utils.tensorboard import SummaryWriter
except ImportError:
    ENABLE_TB = False
    logging.info(
        "tensorboard logging disabled: could not import SummaryWriter: "
        "install tensorboard[python] or shinyutils[pytorch]"
    )
else:
    ENABLE_TB = True

DEFAULT_DEVICE = (
    torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
)


__all__ = ["DEFAULT_DEVICE", "PTOpt", "FCNet", "NNTrainer", "SetTBWriterAction"]


class PTOpt:
    """Wrapper around pytorch optimizer and learning rate scheduler.

    Args:
        weights: Iterable of `Tensor` weights to optimize.
        optim_cls: `Optimizer` class to use.
        optim_params: Mapping of parameters to pass to `optim_cls`.
        lr_sched_cls: `LRScheduler` class to use for scheduling the learning rate.
        lr_sched_params: Mapping of parameters to pass to `lr_sched_cls`.
    """

    def __init__(
        self,
        weights: Iterable[torch.Tensor],
        optim_cls: Type[Optimizer],
        optim_params: Mapping[str, Any],
        lr_sched_cls: Optional[Type[_LRScheduler]] = None,
        lr_sched_params: Optional[Mapping[str, Any]] = None,
    ):
        self.optimizer = optim_cls(weights, **optim_params)
        if lr_sched_cls is None:
            self.lr_sched: Optional[_LRScheduler] = None
        else:
            if lr_sched_params is None:
                lr_sched_params = {}
            self.lr_sched = lr_sched_cls(self.optimizer, **lr_sched_params)

    def __repr__(self) -> str:
        r = repr(self.optimizer)
        if self.lr_sched is not None:
            r += f"\n{self.lr_sched!r}"
        return r

    def zero_grad(self):
        """Call `zero_grad` on underlying optimizer."""
        self.optimizer.zero_grad()

    def step(self):
        """Call `step` on underlying optimizer and lr scheduler (if present)."""
        self.optimizer.step()
        if self.lr_sched is not None:
            self.lr_sched.step()

    @classmethod
    def from_args(
        cls, weights: Iterable[torch.Tensor], args: Namespace, arg_prefix: str = ""
    ) -> "PTOpt":
        """Create `PTOpt` instance from a namespace of arguments.

        Args:
            weights: Iterable of `torch.Tensor` weights to optimize.
            args: Namespace of arguments (argument names are as added by
                `add_parser_args`).
            arg_prefix: Prefix for argument names (default: `""`).
        """
        if arg_prefix:
            arg_prefix += "_"
        argvars = vars(args)
        if f"{arg_prefix}lr_sched_cls" not in argvars:
            argvars[f"{arg_prefix}lr_sched_cls"] = None
            argvars[f"{arg_prefix}lr_sched_params"] = []

        def _eval_key_val_pairs(key_val_pairs):
            _d = {}
            for k, v in key_val_pairs:
                try:
                    _d[k] = int(v)
                except ValueError:
                    try:
                        _d[k] = float(v)  # type: ignore
                    except ValueError:
                        _d[k] = v
            return _d

        return cls(
            weights,
            argvars[f"{arg_prefix}optim_cls"],
            _eval_key_val_pairs(argvars[f"{arg_prefix}optim_params"]),
            argvars[f"{arg_prefix}lr_sched_cls"],
            _eval_key_val_pairs(argvars[f"{arg_prefix}lr_sched_params"]),
        )

    @staticmethod
    def add_parser_args(
        base_parser: Union[ArgumentParser, _ArgumentGroup],
        arg_prefix: str = "",
        group_title: Optional[str] = None,
        default_optim_cls: Optional[Type[Optimizer]] = Adam,
        default_optim_params: Optional[Mapping[str, Any]] = None,
        add_lr_decay: bool = True,
    ) -> Union[ArgumentParser, _ArgumentGroup]:
        """Add options to the base parser for pytorch optimizer and lr scheduling.

        Args:
            base_parser: Argument parser or group to add arguments to.
            arg_prefix: Prefix for argument names (default: empty string).
            group_title: Title to use for added options. If `None`, arguments will be
                added to the base parser. Otherwise, options will be added to a group
                with the given title. A new group will be created if `base_parser` is
                not a group.
            default_optim_cls: Default `Optimizer` class (default: `Adam`).
            default_optim_params: Default set of parameters to pass to the optimizer
                (default: `None`).
            add_lr_decay: Whether to add options for lr decay (default: `True`).

        Example::

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
        """
        if arg_prefix:
            arg_prefix += "-"
        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        opt_sub_cls_type = SubClassType(Optimizer)
        base_parser.add_argument(
            f"--{arg_prefix}optim-cls",
            type=opt_sub_cls_type,
            choices=list(opt_sub_cls_type.choices()),
            required=default_optim_cls is None,
            default=default_optim_cls,
        )

        if default_optim_params is None:
            default_optim_params = {}
        base_parser.add_argument(
            f"--{arg_prefix}optim-params",
            type=KeyValueType(),
            nargs="*",
            default=list(default_optim_params.items()),
        )

        if not add_lr_decay:
            return base_parser

        lr_sched_sub_cls_type = SubClassType(_LRScheduler)
        base_parser.add_argument(
            f"--{arg_prefix}lr-sched-cls",
            type=lr_sched_sub_cls_type,
            choices=list(lr_sched_sub_cls_type.choices()),
            default=None,
        )

        base_parser.add_argument(
            f"--{arg_prefix}lr-sched-params", type=KeyValueType(), nargs="*", default=[]
        )

        return base_parser

    @staticmethod
    def add_help(
        base_parser: Union[ArgumentParser, _ArgumentGroup],
        group_title: Optional[str] = "pytorch help",
    ):
        """Add parser arguments for help on PyTorch optimizers and lr schedulers.

        Args:
            base_parser: `ArgumentParser` or `ArgumentGroup` to add options to.
            group_title: Title for the group of options (default: `pytorch help`).
                If `group_title` is `None`, the options are added to the base parser,
                otherwise they are added to a group (a new one is created if
                `base_parser` is not a group).

        Example::

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
        """

        class _ShowHelp(Action):
            def __call__(self, parser, namespace, values, option_string=None):
                cls_name = values.__name__
                cls_sig = inspect.signature(values)
                print(f"{cls_name}{cls_sig}")
                parser.exit()

        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            "--explain-optimizer",
            type=SubClassType(Optimizer),
            action=_ShowHelp,
            help="describe arguments of a torch optimizer",
        )
        base_parser.add_argument(
            "--explain-lr-sched",
            type=SubClassType(_LRScheduler),
            action=_ShowHelp,
            help="describe arguments of a torch lr scheduler",
        )


class FCNet(nn.Module):
    """Template for a fully connected network.

    Args:
        in_dim: Number of input features.
        out_dim: Number of output features.
        hidden_sizes: List of hidden layer sizes.
        hidden_act: Activation function for hidden layers (default: `relu`).
        out_act: Activation function for output layer (default: `None`).
    """

    _ActType = Callable[[torch.Tensor], torch.Tensor]

    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        hidden_sizes: List[int],
        hidden_act: _ActType = F.relu,
        out_act: Optional[_ActType] = None,
    ):
        super().__init__()
        layer_sizes = [in_dim] + hidden_sizes + [out_dim]
        self.layers = nn.ModuleList(
            [nn.Linear(ls, ls_n) for ls, ls_n in zip(layer_sizes, layer_sizes[1:])]
        )
        self.hidden_act = hidden_act
        self.out_act = out_act

    def __repr__(self):
        out_act_repr = self.out_act.__name__ if self.out_act is not None else "None"
        return (
            "hidden, output activation: "
            + f"{self.hidden_act.__name__}, {out_act_repr}"
            + f"\n{super().__repr__()}"
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Propagate input tensor through the network."""
        for layer in self.layers[:-1]:
            x = self.hidden_act(layer(x))
        x = self.layers[-1](x)
        if self.out_act is not None:
            x = self.out_act(x)
        return x

    @classmethod
    def from_args(cls, args: Namespace, arg_prefix: str = "") -> "FCNet":
        """Create `FCNet` instance from a namespace of arguments.

        Args:
            args: Namespace of arguments, with names as added by `add_parser_args`.
            arg_prefix: Prefix for argument names (default: `""`).
        """
        if arg_prefix:
            arg_prefix += "_"
        argvars = vars(args)
        return cls(
            argvars[f"{arg_prefix}fcnet_indim"],
            argvars[f"{arg_prefix}fcnet_outdim"],
            argvars[f"{arg_prefix}fcnet_hidden_sizes"],
            argvars[f"{arg_prefix}fcnet_hidden_act"],
            argvars[f"{arg_prefix}fcnet_out_act"],
        )

    @staticmethod
    def add_parser_args(
        base_parser: Union[ArgumentParser, _ArgumentGroup],
        arg_prefix: str = "",
        group_title: Optional[str] = None,
        default_indim: Optional[int] = None,
        default_outdim: Optional[int] = None,
        default_hidden_sizes: Optional[int] = None,
        default_hidden_act: Optional[_ActType] = F.relu,
        default_out_act: Optional[_ActType] = None,
    ):
        """Add options to a parser for building a `FCNet` object.

        Args:
            base_parser: `ArgumentParser` or `ArgumentGroup` to add options to.
            arg_prefix: Prefix for argument names (default: `""`).
            group_title: Title for the group of options If `None` (the default),
                the options are added to the base parser. Otherwise they are added
                to a group with the given title (a new one is created if `base_parser`
                is not a group).
            default_indim: Default value for `indim` (default: `None`).
            default_outdim: Default value for `outdim` (default: `None`).
            default_hidden_sizes: Default value for `hidden_sizes` (default: `None`).
            default_hidden_act: Default value for hidden activation (default: `relu`).
            default_out_act: Default value for output activation (default: `None`).

        Example::

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
        """

        class _Act:
            __metavar__ = "func"

            def __call__(self, string):
                try:
                    return getattr(F, string)
                except AttributeError:
                    raise ArgumentTypeError(
                        f"invalid activation function: {string}"
                    ) from None

        if arg_prefix:
            arg_prefix += "-"
        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            f"--{arg_prefix}fcnet-indim",
            type=int,
            required=default_indim is None,
            default=default_indim,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-outdim",
            type=int,
            required=default_outdim is None,
            default=default_outdim,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-hidden-sizes",
            type=int,
            nargs="+",
            required=default_hidden_sizes is None,
            default=default_hidden_sizes,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-hidden-act",
            type=_Act(),
            required=default_hidden_act is None,
            default=default_hidden_act,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-out-act",
            type=_Act(),
            required=False,
            default=default_out_act,
        )


class NNTrainer:
    """Helper class for training a model on a dataset.

    Args:
        batch_size: Batch size for training.
        data_load_workers: Number of workers for loading data (default: `0`).
        shuffle: Whether to shuffle the data (default: `True`).
        pin_memory: When to pin data to CUDA memory (default: `True`).
        drop_last: Whether to drop the last incomplete batch (default: `True`).
        device: Device to use for training (default: `cuda` if available, else `cpu`).
    """

    def __init__(
        self,
        batch_size: int,
        data_load_workers: int = 0,
        shuffle: bool = True,
        pin_memory: bool = True,
        drop_last: bool = True,
        device: torch.device = DEFAULT_DEVICE,
    ):
        self._batch_size = batch_size
        self._data_load_workers = data_load_workers
        self._shuffle = shuffle
        self._pin_memory = pin_memory
        self._drop_last = drop_last
        self._device: torch.device = device

        self._dataset: Dataset
        self._data_loader: DataLoader

    @overload
    def set_dataset(self, value: Dataset):
        ...

    @overload
    def set_dataset(self, value: Tuple[torch.Tensor, ...]):
        ...

    @overload
    def set_dataset(self, value: Tuple[np.ndarray, ...]):
        ...

    def set_dataset(self, value):
        """Set the training data.

        Args:
            value: `torch.utils.data.Dataset` instance, or tuple of `torch.Tensor` or
                `np.ndarray` objects.
        """
        if isinstance(value, Dataset):
            self._dataset = value
        elif isinstance(value, tuple):
            if isinstance(value[0], np.ndarray):
                value = [torch.from_numpy(val_i) for val_i in value]
            self._dataset = TensorDataset(*value)
        else:
            raise ValueError(f"can't set dataset from type {type(value)}")

        self._data_loader = DataLoader(
            self._dataset,
            self._batch_size,
            self._shuffle,
            num_workers=self._data_load_workers,
            pin_memory=self._pin_memory,
            drop_last=self._drop_last,
        )

    def train(
        self,
        model: nn.Module,
        opt: PTOpt,
        loss_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
        iters: int,
        pbar_desc: str = "Training",
    ):
        """Train a model.

        Args:
            model: Model (`nn.Module` instance) to train.
            opt: `PTOpt` instance to use for optimizing.
            loss_fn: Loss function mapping input tensors to a loss tensor.
            iters: Number of iterations to train for.
            pbar_desc: Description for progress bar (default: `Training`).
        """
        if self._dataset is None:
            raise RuntimeError("dataset not set: call set_dataset before train")
        bat_iter = iter(self._data_loader)

        logging.info("moving model to %s", self._device)
        model = model.to(self._device)

        with trange(iters, desc=pbar_desc) as pbar:
            for _ in pbar:
                try:
                    x_bat, y_bat = next(bat_iter)
                except StopIteration:
                    bat_iter = iter(self._data_loader)
                    x_bat, y_bat = next(bat_iter)
                x_bat, y_bat = x_bat.to(self._device), y_bat.to(self._device)

                yhat_bat = model(x_bat)
                loss = loss_fn(yhat_bat, y_bat)
                pbar.set_postfix(loss=float(loss))

                opt.zero_grad()
                loss.backward()
                opt.step()


class SetTBWriterAction(Action):
    """`argparse.Action` to set the `tb_writer` attribute.

    The attribute (configurable via `SetTBWriterAction.attr`) is set to a
    `SummaryWriter`, or a `Mock` of the class (if called without any value).

    Usage::

        arg_parser = ArgumentParser()
        arg_parser.add_argument(
            "--tb-dir",
            type=str,
            action=SetTBWriterAction,
        )
        arg_parser.set_defaults(tb_writer=Mock(SummaryWriter))
        args = arg_parser.parse_args(["--tb-dir", "tmp/tb"])
        args.tb_writer  # `SummaryWriter` instance
    """

    attr = "tb_writer"

    def __call__(self, parser, namespace, values, option_strings=None):
        if values is None:
            values = Mock(SummaryWriter)
        else:
            values = SummaryWriter(values)
        setattr(namespace, SetTBWriterAction.attr, values)


def _better_lr_sched_repr(lr_sched: _LRScheduler):
    return (
        lr_sched.__class__.__name__
        + "(\n    "
        + "\n    ".join(
            f"{k}: {v}"
            for k, v in lr_sched.state_dict().items()
            if not k.startswith("_")
        )
        + "\n)"
    )


setattr(_LRScheduler, "__repr__", _better_lr_sched_repr)
