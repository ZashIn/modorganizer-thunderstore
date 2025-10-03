from collections.abc import Mapping
from dataclasses import MISSING, fields
from typing import Any, ClassVar, Protocol

import mobase


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]


def dataclass_from_dict[DataClass: DataclassInstance](
    cls: type[DataClass], d: Mapping[str, Any]
) -> DataClass:
    """
    Construct the given dataclass from a dict, ignoring extra keys or missing optional args.

    Raises:
        TypeError: for missing required field
    """
    return cls(
        **{
            f.name: value
            for f in fields(cls)
            if f.init and (value := d.get(f.name, MISSING)) is not MISSING
        }
    )


def hide_file_tree_entry(
    tree: mobase.IFileTree,
    entry: mobase.FileTreeEntry,
    hidden_suffix: str = ".mohidden",
):
    return tree.move(entry, add_hidden_suffix(entry, hidden_suffix))


def add_hidden_suffix(
    entry: mobase.FileTreeEntry, hidden_suffix: str = ".mohidden"
) -> str:
    entry_name = entry.name()
    if (old_suffix := f".{entry.suffix()}") != ".":
        entry_name = entry_name[: -len(old_suffix)]
    return f"{entry_name}{hidden_suffix}{old_suffix}"
