from pathlib import Path

import mobase
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon

from .base import ThunderstoreBasePlugin


class ThunderstoreModPage(ThunderstoreBasePlugin, mobase.IPluginModPage):
    def __init__(self) -> None:
        super().__init__()
        mobase.IPluginModPage.__init__(self)

    def displayName(self) -> str:
        return f"Visit {self.get_community_name()} on {self.domain}"

    def handlesDownload(
        self, page_url: QUrl, download_url: QUrl, fileinfo: mobase.ModRepositoryFileInfo
    ) -> bool:
        # BUG (MO): internal browser does handle downloads, this function is never called!
        if self.pageURL().isParentOf(page_url):
            # BUG (MO): fileinfo cannot be changed from Python
            # https://github.com/ModOrganizer2/modorganizer/issues/2286
            # https://github.com/ModOrganizer2/modorganizer/blob/8016e77723b7de88a3900ad3f47efc73edc66fae/src/downloadmanager.cpp#L1076-L1079
            # https://github.com/ModOrganizer2/modorganizer-plugin_python/blob/6bed428d04dce605a6ef0b71200d7a62a8a0bd9b/src/mobase/wrappers/pyplugins.h#L229
            return True
        return False

    def icon(self: mobase.IPluginModPage) -> QIcon:
        return QIcon(str(Path(__file__).with_name("thunderstore_icon.png").resolve()))

    def pageURL(self) -> QUrl:
        return QUrl(f"{self.base_url}/c/{self.get_community_name()}")

    def useIntegratedBrowser(self: mobase.IPluginModPage) -> bool:
        return False  # BUG (MO): internal browser does handle downloads
