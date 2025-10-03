from collections.abc import Sequence

import mobase


class ThunderstoreBasePlugin(mobase.IPlugin):
    base_name = "Thunderstore"
    domain = "thunderstore.io"
    base_url = f"https://{domain}"

    community_name = ""
    """Thunderstore community name, see `.get_community_name()`."""

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

    def settings(self) -> Sequence[mobase.PluginSetting]:
        return [
            mobase.PluginSetting(
                "thunderstore_community",
                (
                    "Set/overwrite the current thunderstore community."
                    " By default it is retrieved from the game plugin."
                ),
                self.community_name,
            ),
        ]

    def get_community_name(self) -> str:
        """
        Thunderstore community name (from url `/c/<community>`) for page and mod URL.
        The community name can be set by / is checked in this order:
        - Setting `thunderstore_community` on this plugin or the game plugin.
        - Adding a `GameThunderstoreName` attribute or `gameThunderstoreName()` method to `mobase.IPluginGame`.
        - Setting the `community_name` attribute.
        """
        # from plugin setting
        if community_name := self._organizer.pluginSetting(
            self.base_name, "thunderstore_community"
        ):
            return str(community_name)
        game = self._organizer.managedGame()
        # from game plugin setting
        if community_name := self._organizer.pluginSetting(
            game.name(), "thunderstore_community"
        ):
            return str(community_name)
        # from game plugin attribute / method
        if community_name := getattr(
            game,
            "gameThunderstoreName",
            getattr(game, "GameThunderstoreName", self.community_name),
        ):
            if isinstance(community_name, str) or (
                callable(community_name)
                and isinstance(community_name := community_name(), str)
            ):
                return community_name
        return self.community_name
