import re
from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass
class ThunderStoreModInfo:
    full_name: str
    namespace: str
    name: str
    version: str

    def get_url(self, base_url: str, community: str):
        return f"{base_url}/c/{community}/p/{self.namespace}/{self.name}/"


    @classmethod
    def from_file_path(cls, str_path: str | Path) -> Self | None:
        if isinstance(str_path, str):
            str_path = Path(str_path)
        return cls.parse_dependency_str(str_path.name)

    @classmethod
    def parse_dependency_str(cls, name: str) -> Self | None:
        """
        Parse thunderstore dependency string or file name, e.g. `"namespace-name-1.0.0"`.
        """
        if match := re.match(
            r"^(?P<full_name>(?P<namespace>.+?)-(?P<name>.+?))-(?P<version>[\d\.]+\d)",
            name,
        ):
            return cls(**match.groupdict())
        return None
