from collections.abc import Sequence

import mobase


class ThunderstoreBasePlugin(mobase.IPlugin):
    base_name = "Thunderstore"
    domain = "thunderstore.io"
    base_url = f"https://{domain}"

    _organizer: mobase.IOrganizer

    def init(self, organizer: mobase.IOrganizer) -> bool:
        self._organizer = organizer
        return True

    def name(self) -> str:
        return self.base_name

    def version(self: mobase.IPlugin) -> mobase.VersionInfo:
        return mobase.VersionInfo(0, 1, 0)

    def author(self: mobase.IPlugin) -> str:
        return "Zash"

    def description(self) -> str:
        return f"Adds support for {self.domain} mod page."

    def settings(self: mobase.IPlugin) -> Sequence[mobase.PluginSetting]:
        return []
