import re
from dataclasses import (
    MISSING,
    dataclass,
    fields,
)
from pathlib import Path
from typing import Any, Mapping


@dataclass
class ThunderStoreModInfo:
    full_name: str
    namespace: str
    name: str
    version: str

    def get_url(self, community: str, base_url: str = "https://thunderstore.io"):
        return f"{base_url}/c/{community}/p/{self.namespace}/{self.name}/"

    @classmethod
    def from_file_path(cls, file_path: Path):
        if match := cls.parse_file_name(file_path.name):
            return cls.from_dict(match.groupdict())
        return None

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]):
        try:
            return cls(
                **{
                    f.name: (
                        d[f.name] if f.default is MISSING else d.get(f.name, f.default)
                    )
                    for f in fields(cls)
                    if f.init
                }
            )
        except KeyError:
            return None

    @classmethod
    def parse_file_name(cls, filename: str) -> re.Match[str] | None:
        if match := re.match(
            r"(?P<full_name>(?P<namespace>.+?)-(?P<name>.+?))-(?P<version>[\d\.]+)\.[^.]+$",
            filename,
        ):
            return match
        return None
