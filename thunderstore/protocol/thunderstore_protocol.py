import re
from typing import Self

THUNDERSTORE_SCHEME = "ror2mm"


class ThunderstoreProtocol:
    scheme = THUNDERSTORE_SCHEME
    url_base = f"{scheme}://v1/install/"
    url_pattern = re.compile(rf"{scheme}://v1/install/(?P<host>[^/]+)/(?P<path>.+)$")

    def __init__(self, host: str, path: str) -> None:
        self.host: str = host
        self.path: str = path

    @classmethod
    def parse_url(cls, url: str) -> Self:
        if not (match := cls.url_pattern.match(url)):
            raise ValueError(
                f'Unsupported URL "{url}", required protocol: {cls.url_base}'
            )
        return cls(match["host"], match["path"])

    def get_download_url(self):
        return f"https://{self.host}/package/download/{self.path}"
