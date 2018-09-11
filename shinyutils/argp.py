"""argp.py: utilities for argparse."""

from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentTypeError,
    MetavarTypeHelpFormatter,
)
import re

import crayons


class LazyHelpFormatter(
    ArgumentDefaultsHelpFormatter, MetavarTypeHelpFormatter
):

    DEF_PAT = re.compile(r"(\(default: (.*?)\))")
    TYPE_PAT = re.compile(r"\b(int|float|str)\b")
    DEF_CSTR = str(crayons.magenta("default"))

    def _format_action(self, action):
        if not action.help:
            action.help = "\b"
        astr = super()._format_action(action)

        m = re.search(self.DEF_PAT, astr)
        if m:
            mstr, dstr = m.groups()
            astr = astr.replace(
                mstr, f"({self.DEF_CSTR}: {crayons.magenta(dstr, bold=True)})"
            )

        m = re.findall(self.TYPE_PAT, astr)
        for dstr in m:
            astr = astr.replace(dstr, str(crayons.red(dstr, bold=True)))

        return astr

    def _get_default_metavar_for_optional(self, action):
        if action.type:
            return action.type.__name__

    def _get_default_metavar_for_positional(self, action):
        if action.type:
            return action.type.__name__


def comma_separated_ints(string):
    try:
        return list(map(int, string.split(",")))
    except:
        raise ArgumentTypeError(
            f"`{string}` is not a comma separated list of ints"
        )
