"""subcls.py: utility functions for dealing with subclasses."""

from typing import List, Type, TypeVar

__all__ = [
    "get_subclasses",
    "get_subclass_names",
    "get_subclass_from_name",
]

T = TypeVar("T")


def get_subclasses(cls: Type[T]) -> List[Type[T]]:
    """Get all subclasses (even indirect) of the given class."""
    subclasses = []
    for c in cls.__subclasses__():
        subclasses.append(c)
        subclasses.extend(get_subclasses(c))
    return subclasses


def get_subclass_names(cls: Type[T]) -> List[str]:
    """Get the names of all subclasses of the given class."""
    return [c.__name__ for c in get_subclasses(cls)]


def get_subclass_from_name(base_cls: Type[T], cls_name: str) -> Type[T]:
    """Get a subclass given its name."""
    for c in get_subclasses(base_cls):
        if c.__name__ == cls_name:
            return c
    raise RuntimeError("No such subclass of {}: {}".format(base_cls.__name__, cls_name))
