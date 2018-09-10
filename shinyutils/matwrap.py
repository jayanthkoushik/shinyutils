"""matwrap.py: wrapper around matplotlib."""
import json
from pkg_resources import resource_filename


class MatWrap:

    _rc_defaults_path = resource_filename("shinyutils", "data/mplcfg.json")
    with open(_rc_defaults_path, "r") as f:
        _rc_defaults = json.load(f)

    _mpl = None
    _plt = None
    _sns = None

    @classmethod
    def configure(cls, context="paper", style="ticks", **rc_extra):
        """
        Arguments:
            context: seaborn context (paper/notebook/poster).
            rc_extra: matplotlib params (will overwrite defaults).
        """
        rc = MatWrap._rc_defaults.copy()
        rc.update(rc_extra)

        if cls._mpl is None:
            import matplotlib

            cls._mpl = matplotlib
            cls._mpl.rcParams.update(rc)

            import matplotlib.pyplot
            import seaborn

            cls._plt = matplotlib.pyplot
            cls._sns = seaborn
        else:
            cls._mpl.rcParams.update(rc)
        cls._sns.set(context, style, rc=rc)

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
        cls._ensure_conf()
        return cls._mpl

    @classmethod
    def plt(cls):
        cls._ensure_conf()
        return cls._plt

    @classmethod
    def sns(cls):
        cls._ensure_conf()
        return cls._sns

    @staticmethod
    def set_size_tight(fig, size):
        fig.set_size_inches(*size)
        fig.tight_layout(pad=0, w_pad=0, h_pad=0)
