"""argp.py: utilities for argparse."""

import logging
import os
from argparse import ArgumentTypeError, FileType
from pathlib import Path
from typing import Dict, Generic, IO, List, Optional, Type, TypeVar, Union

from shinyutils._subcls import get_subclass_from_name, get_subclass_names

__all__ = [
    "CommaSeparatedInts",
    "InputFileType",
    "OutputFileType",
    "InputDirectoryType",
    "OutputDirectoryType",
    "ClassType",
    "KeyValuePairsType",
]


class CommaSeparatedInts:

    __metavar__ = "int,[...]"

    def __call__(self, string: str) -> List[int]:
        try:
            return list(map(int, string.split(",")))
        except:
            raise ArgumentTypeError(
                f"`{string}` is not a comma separated list of ints"
            ) from None


class InputFileType(FileType):

    __metavar__ = "file"

    def __init__(
        self,
        mode: str = "r",
        bufsize: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
    ) -> None:
        if mode not in {"r", "rb"}:
            raise ValueError("mode should be 'r'/'rb'")
        super().__init__(mode, bufsize, encoding, errors)

    def __call__(self, string: str) -> IO:
        # pylint: disable=useless-super-delegation
        return super().__call__(string)


class OutputFileType(FileType):

    __metavar__ = "file"

    def __init__(
        self,
        mode: str = "w",
        bufsize: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
    ) -> None:
        if mode not in {"w", "wb"}:
            raise ValueError("mode should be 'w'/'wb'")
        super().__init__(mode, bufsize, encoding, errors)

    def __call__(self, string: str) -> IO:
        file_dir = os.path.dirname(string)
        if file_dir and not os.path.exists(file_dir):
            logging.warning("no directory for %s: trying to create", string)
            try:
                os.makedirs(file_dir)
            except Exception as e:
                raise ArgumentTypeError(f"could not create {file_dir}") from e
            logging.info("created %s", file_dir)
        return super().__call__(string)


class InputDirectoryType:

    __metavar__ = "dir"

    def __call__(self, string: str) -> Path:
        if not os.path.exists(string):
            raise ArgumentTypeError(f"no such directory: {string}")
        if not os.path.isdir(string):
            raise ArgumentTypeError(f"{string} is a file: expected directory")
        return Path(string)


class OutputDirectoryType:

    __metavar__ = "dir"

    def __call__(self, string: str) -> Path:
        if not os.path.exists(string):
            logging.warning("%s not found: trying to create", string)
            try:
                os.makedirs(string)
            except Exception as e:
                raise ArgumentTypeError("cound not create %s" % string) from e
            logging.info("created %s", string)
        elif not os.path.isdir(string):
            raise ArgumentTypeError(f"{string} is a file: expected directory")
        return Path(string)


T = TypeVar("T")


class ClassType(Generic[T]):

    __metavar__ = "cls"

    def __init__(self, cls: Type[T]) -> None:
        self.cls = cls

    def __call__(self, string: str) -> Type[T]:
        try:
            return get_subclass_from_name(self.cls, string)
        except RuntimeError:
            choices = [f"'{c}'" for c in get_subclass_names(self.cls)]
            raise ArgumentTypeError(
                f"invalid choice: '{string}' " f"(choose from {', '.join(choices)})"
            ) from None


class KeyValuePairsType:

    __metavar__ = "str=val[,...]"
    ValType = Union[int, float, str]

    def __call__(self, string: str) -> Dict[str, ValType]:
        out = dict()
        try:
            for kv in string.split(","):
                k, v = kv.split("=")
                pv: KeyValuePairsType.ValType = v
                try:
                    pv = int(v)
                except ValueError:
                    try:
                        pv = float(v)
                    except ValueError:
                        pass
                out[k] = pv
        except Exception as e:
            raise ArgumentTypeError() from e
        return out
