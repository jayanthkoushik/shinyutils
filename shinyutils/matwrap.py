"""Utilities for matplotlib and seaborn."""

import json
import warnings
from argparse import _ArgumentGroup, Action, ArgumentParser
from contextlib import AbstractContextManager
from typing import Any, List, Mapping, Optional, Tuple, Union

from corgy.types import KeyValueType
from pkg_resources import resource_filename

_WRAPPED_NAMES = ["mpl", "plt", "sns"]  # pylint: disable=undefined-all-variable
__all__ = ["MatWrap", "Plot"] + _WRAPPED_NAMES


def __getattr__(name):
    if name in _WRAPPED_NAMES:
        attr = getattr(MatWrap, name)
        return attr.__func__(MatWrap)
    raise AttributeError


class MatWrap:
    """Wrapper for `matplotlib`, `matplotlib.pyplot`, and `seaborn`.

    Usage::

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
    """

    _rc_defaults_path = resource_filename("shinyutils", "data/mplcfg.json")
    with open(_rc_defaults_path, "r", encoding="utf-8") as f:
        _rc_defaults = json.load(f)

    _mpl = None
    _plt = None
    _sns = None

    _args: Mapping[str, Any]
    _mpl_default_rc: Mapping[str, Any]

    @classmethod
    def configure(
        cls,
        context: str = "paper",
        style: str = "ticks",
        font: str = "Latin Modern Roman",
        latex_pkgs: Optional[List[str]] = None,
        **rc_extra,
    ):
        """Configure matplotlib and seaborn.

        Args:
            context: Seaborn context ([`paper`]/`poster`/`notebook`).
            style: Seaborn style (`darkgrid`/`whitegrid`/`dark`/`white`/[`ticks`]).
            font: Font, passed directly to fontspec (default: `Latin Modern Roman`).
            latex_pkgs: List of packages to load in latex pgf preamble.
            rc_extra: Matplotlib params (will overwrite defaults).
        """
        rc = MatWrap._rc_defaults.copy()
        rc["pgf.preamble"] = [r"\usepackage{fontspec}"]
        rc["pgf.preamble"].append(rf"\setmainfont{{{font}}}")
        rc["pgf.preamble"].append(rf"\setsansfont{{{font}}}")
        if latex_pkgs is not None:
            for pkg in reversed(latex_pkgs):
                rc["pgf.preamble"].insert(0, rf"\usepackage{{{pkg}}}")
        rc["pgf.preamble"] = "\n".join(rc["pgf.preamble"])
        rc.update(rc_extra)

        if cls._mpl is None:
            # pylint: disable=import-outside-toplevel
            try:
                import matplotlib
            except ImportError as e:
                e.msg += ": install shinyutils[plotting] to use MatWrap"
                raise e

            cls._mpl = matplotlib
            cls._mpl_default_rc = cls._mpl.rcParams.copy()
            cls._mpl.rcParams.update(rc)

            import matplotlib.pyplot

            try:
                import seaborn
            except ImportError as e:
                e.msg += ": install shinyutils[plotting] to use MatWrap"
                raise e

            cls._plt = matplotlib.pyplot
            cls._sns = seaborn
        else:
            cls._mpl.rcParams = cls._mpl_default_rc.copy()
            cls._mpl.rcParams.update(rc)

        if "font.size" in rc:
            font_scale = rc["font.size"] / cls._mpl_default_rc["font.size"]
        else:
            font_scale = 1
        cls._sns.set(context, style, cls.palette(), font_scale=font_scale, rc=rc)

        cls._args = rc_extra.copy()
        cls._args["context"] = context
        cls._args["style"] = style
        cls._args["font"] = font
        cls._args["latex_pkgs"] = latex_pkgs

    def __new__(cls):
        raise NotImplementedError(
            "MatWrap does not provide instances. Use the class methods."
        )

    @classmethod
    def _ensure_conf(cls):
        if cls._mpl is None:
            cls.configure()

    @classmethod
    def mpl(cls):
        """`matplotlib` module."""
        cls._ensure_conf()
        assert cls._mpl is not None
        return cls._mpl

    @classmethod
    def plt(cls):
        """`matplotlib.pyplot` module."""
        cls._ensure_conf()
        assert cls._plt is not None
        return cls._plt

    @classmethod
    def sns(cls):
        """`seaborn` module."""
        cls._ensure_conf()
        assert cls._sns is not None
        return cls._sns

    @classmethod
    def palette(cls) -> List[str]:
        """Color-blindness friendly palette of 8 colors in hex."""
        return [
            "#e41a1c",
            "#6a3d9a",
            "#d55e00",
            "#34495e",
            "#377eb8",
            "#4daf4a",
            "#95a5a6",
            "#222222",
        ]

    @staticmethod
    def set_size_tight(fig, size: Tuple[int, int]):
        """Set the size of a matplotlib figure.

        Args:
            fig: Matplotlib `Figure` instance.
            size: Tuple (width, height) in inches.
        """
        warnings.warn(
            "constrained_layout is enabled by default: don't use tight_layout",
            FutureWarning,
        )
        fig.set_size_inches(*size)
        fig.tight_layout(pad=0, w_pad=0, h_pad=0)

    @staticmethod
    def add_parser_config_args(
        base_parser: Union[ArgumentParser, _ArgumentGroup],
        group_title: Optional[str] = "plotting options",
    ) -> Union[ArgumentParser, _ArgumentGroup]:
        """Add arguments for configuring plotting to a parser.

        Args:
            base_parser: Argument parser or group to add arguments to.
            group_title: Title to use for added options. If `None`, arguments will be
                added to the base parser. Otherwise, options will be added to a group
                with the given title. A new group will be created if `base_parser` is
                not a group.

        Example::

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
        """

        class _ConfMatwrap(Action):
            def __call__(self, parser, namespace, values, option_string=None):
                _args = MatWrap._args
                assert option_string.startswith("--plotting-")
                option_name = option_string.split("--plotting-")[1].replace("-", "_")
                if option_name == "rc_extra":
                    _d = {}
                    for k, v in values:
                        try:
                            _d[k] = int(v)
                        except ValueError:
                            try:
                                _d[k] = float(v)
                            except ValueError:
                                _d[k] = v
                    MatWrap.configure(**_args, **dict(values))
                else:
                    assert option_name in _args
                    _args[option_name] = values
                    MatWrap.configure(**_args)

        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            "--plotting-context",
            type=str,
            choices=["paper", "notebook", "talk", "poster"],
            default="paper",
            action=_ConfMatwrap,
        )
        base_parser.add_argument(
            "--plotting-style",
            type=str,
            choices=["white", "dark", "whitegrid", "darkgrid", "ticks"],
            default="ticks",
            action=_ConfMatwrap,
        )
        base_parser.add_argument(
            "--plotting-font",
            type=str,
            default="Latin Modern Roman",
            action=_ConfMatwrap,
        )
        base_parser.add_argument(
            "--plotting-latex-pkgs",
            type=str,
            nargs="*",
            default=[],
            action=_ConfMatwrap,
        )
        base_parser.add_argument(
            "--plotting-rc-extra",
            type=KeyValueType(),
            nargs="*",
            default=[],
            action=_ConfMatwrap,
        )

        return base_parser


class Plot(AbstractContextManager):
    """Wrapper around a single matplotlib plot.

    This class is a context manager that returns a matplotlib `axis` instance when
    entering the context. The plot is closed, and optionally, saved to a file when
    exiting the context.

    Args:
        save_file: Path to save plot to. If `None` (the default), the plot is not
            saved.
        title: Optional title for plot.
        sizexy: Size tuple (width, height) in inches. If `None` (the default), the
            plot size will be determined automatically by matplotlib.
        labelxy: Tuple of labels for the x and y axes respectively. If either value is
            `None` (the default), the corresponding axis will not be labeled.
        logxy: Tuple of booleans indicating whether to use a log scale for the x and y
            axis respectively (default: `(False, False)`).

    Usage::

        with Plot() as ax:
            # Use `ax` to plot stuff.
            ...
    """

    def __init__(
        self,
        save_file: Optional[str] = None,
        title: Optional[str] = None,
        sizexy: Optional[Tuple[int, int]] = None,
        labelxy: Tuple[Optional[str], Optional[str]] = (None, None),
        logxy: Tuple[bool, bool] = (False, False),
    ):
        self.save_file = save_file
        self.title = title
        self.sizexy = sizexy
        self.labelxy = labelxy

        self.fig = MatWrap.plt().figure()
        self.ax = self.fig.add_subplot(111)

        if logxy[0] is True:
            self.ax.set_xscale("log", nonposx="clip")
        if logxy[1] is True:
            self.ax.set_yscale("log", nonposy="clip")

    def __enter__(self):
        return self.ax

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            return

        if self.title is not None:
            self.ax.set_title(self.title)

        if self.labelxy[0] is not None:
            self.ax.set_xlabel(self.labelxy[0])
        if self.labelxy[1] is not None:
            self.ax.set_ylabel(self.labelxy[1])

        if self.sizexy is not None:
            self.fig.set_size_inches(*self.sizexy)

        if self.save_file is not None:
            self.fig.savefig(self.save_file)
        MatWrap.plt().close(self.fig)


MatWrap.configure()
