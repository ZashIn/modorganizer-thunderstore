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
    hidden_suffix: str = "mohidden",
):
    if entry.suffix() == hidden_suffix:
        return True
    return tree.move(entry, f"{entry.name()}.{hidden_suffix}")
