"""argp.py: utilities for argparse."""

from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentTypeError,
    MetavarTypeHelpFormatter,
    FileType,
)
import logging
import os
from pathlib import Path
import re
from unittest.mock import patch

import crayons

from shinyutils.subcls import get_subclass_from_name, get_subclass_names


class LazyHelpFormatter(ArgumentDefaultsHelpFormatter, MetavarTypeHelpFormatter):

    # pylint: disable=no-member
    DEF_PAT = re.compile(r"(\(default: (.*?)\))")
    DEF_CSTR = str(crayons.magenta("default"))

    def _format_action(self, action):
        if action.dest == "help" and self.disable_help_usage:
            return ""

        helpstr = action.help
        action.help = "\b"

        if action.nargs == 0:
            # hack to fix length of option strings
            action.option_strings[0] += str(crayons.normal("", bold=True))
        astr = super()._format_action(action)
        if not action.option_strings:
            astr = astr[:-1]

        m = re.search(self.DEF_PAT, astr)
        if m:
            mstr, dstr = m.groups()
            astr = astr.replace(
                mstr, f"({self.DEF_CSTR}: {crayons.magenta(dstr, bold=True)})"
            )

        if helpstr:
            astr += f"\t{helpstr}\n"

        # add choices to help
        if action.choices:
            choice_strs = [str(crayons.green(c, bold=True)) for c in action.choices]
            astr += f"\t{' / '.join(choice_strs)}\n"

        if not astr.endswith("\n"):
            astr += "\n"

        return astr

    def _format_action_invocation(self, action):
        if action.option_strings and action.nargs != 0:
            # show action as -s/--long ARGS rather than -s ARGS, --long ARGS
            combined_opt_strings = "/".join(action.option_strings)
            with patch.object(action, "option_strings", [combined_opt_strings]):
                return super()._format_action_invocation(action)

        with patch.object(  # format positional arguments same as optional
            action, "option_strings", action.option_strings or [action.dest]
        ):
            return super()._format_action_invocation(action)

    def _get_default_metavar_for_optional(self, action):
        if action.type:
            try:
                return action.type.__name__
            except AttributeError:
                return type(action.type).__name__
        return None

    def _get_default_metavar_for_positional(self, action):
        if action.type:
            try:
                return action.type.__name__
            except AttributeError:
                return type(action.type).__name__
        return None

    def _metavar_formatter(self, action, default_metavar):
        with patch.object(action, "choices", None):
            base_formatter = super()._metavar_formatter(action, default_metavar)

        def color_wrapper(tuple_size):
            f = base_formatter(tuple_size)
            if not f:
                return f
            return (
                str(crayons.red(" ".join(map(str, f)), bold=True)),
                *(("",) * (len(f) - 1)),
            )

        return color_wrapper

    def __init__(self, *args, disable_help_usage=True, **kwargs):
        if "max_help_position" not in kwargs:
            kwargs["max_help_position"] = float("inf")
        if "width" not in kwargs:
            kwargs["width"] = float("inf")
        super().__init__(*args, **kwargs)
        self.disable_help_usage = disable_help_usage

    def add_usage(self, *args, **kwargs):
        pass


def comma_separated_ints(string):
    try:
        return list(map(int, string.split(",")))
    except:
        raise ArgumentTypeError(f"`{string}` is not a comma separated list of ints")


class InputFileType(FileType):
    def __init__(self, mode="r", **kwargs):
        if mode not in {"r", "rb"}:
            raise ValueError("mode should be 'r'/'rb'")
        super().__init__(mode, **kwargs)


class OutputFileType(FileType):
    def __init__(self, mode="w", **kwargs):
        if mode not in {"w", "wb"}:
            raise ValueError("mode should be 'w'/'wb'")
        super().__init__(mode, **kwargs)

    def __call__(self, string):
        file_dir = os.path.dirname(string)
        if file_dir and not os.path.exists(file_dir):
            logging.warning(f"no directory for {string}: trying to create")
            try:
                os.makedirs(file_dir)
            except Exception as e:
                raise ArgumentTypeError(f"could not create {file_dir}: {e}")
            logging.info(f"created {file_dir}")
        return super().__call__(string)


class InputDirectoryType:
    def __call__(self, string):
        if not os.path.exists(string):
            raise ArgumentTypeError(f"no such directory: {string}")
        return Path(string)


class OutputDirectoryType:
    def __call__(self, string):
        if not os.path.exists(string):
            logging.warning(f"{string} not found: trying to create")
            try:
                os.makedirs(string)
            except Exception as e:
                raise ArgumentTypeError(f"cound not create {string}: {e}")
            logging.info(f"created {string}")
        return Path(string)


class ClassType:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, string):
        try:
            return get_subclass_from_name(self.cls, string)
        except RuntimeError:
            choices = [f"'{c}'" for c in get_subclass_names(self.cls)]
            raise ArgumentTypeError(
                f"invalid choice: '{string}' " f"(choose from {', '.join(choices)})"
            )


class KeyValuePairsType:
    def __call__(self, string):
        out = dict()
        try:
            for kv in string.split(","):
                k, v = kv.split("=")
                try:
                    v = int(v)
                except ValueError:
                    try:
                        v = float(v)
                    except ValueError:
                        pass
                out[k] = v
        except Exception as e:
            raise ArgumentTypeError(e)
        return out
