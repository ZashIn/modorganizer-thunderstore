from collections.abc import Sequence
from pathlib import Path

import mobase
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon

from .community import ThunderStoreCommunity
from .modinfo import ThunderStoreModInfo


class ThunderstoreModPage(mobase.IPluginModPage):
    domain = "thunderstore.io"
    base_url = f"https://{domain}"

    _organizer: mobase.IOrganizer
    community: ThunderStoreCommunity

    def __init__(self) -> None:
        super().__init__()
        self.community = ThunderStoreCommunity()

    def name(self) -> str:
        return self.domain

    def version(self: mobase.IPlugin) -> mobase.VersionInfo:
        return mobase.VersionInfo(0, 1, 0)

    def author(self: mobase.IPlugin) -> str:
        return "Zash"

    def description(self: mobase.IPlugin) -> str:
        return "Adds support for thunderstore.io mod page"

    def init(self, organizer: mobase.IOrganizer) -> bool:
        self._organizer = organizer
        self._organizer.modList().onModInstalled(self.update_mod_info_from_file)
        return True

    def displayName(self) -> str:
        return f"Visit {self._organizer.managedGame().gameShortName()} on Thunderstore"

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
        return QUrl(f"{self.base_url}/c/{self.get_community_name}")

    def useIntegratedBrowser(self: mobase.IPluginModPage) -> bool:
        return False  # BUG (MO): internal browser does handle downloads

    def settings(self: mobase.IPlugin) -> Sequence[mobase.PluginSetting]:
        return []

    def get_community_name(self) -> str:
        return self.community.get_community_name(self._organizer.managedGame())

    def update_mod_info_from_file(self, mod: mobase.IModInterface, force: bool = False):
        if not force:
            if mod.nexusId() or mod.isSeparator() or mod.isBackup() or mod.isForeign():
                return
            if (url := mod.url()) and not url.startswith(self.base_url):
                return
        if ts_mod_info := self.get_thunderstore_modinfo(mod):
            mod.setVersion(mobase.VersionInfo(ts_mod_info.version))
            mod.setUrl(ts_mod_info.get_url(self.get_community_name()))

    def get_thunderstore_modinfo(self, mod: mobase.IModInterface):
        if install_file := mod.installationFile():
            if ts_mod_info := ThunderStoreModInfo.from_file_path(Path(install_file)):
                return ts_mod_info
        return None
