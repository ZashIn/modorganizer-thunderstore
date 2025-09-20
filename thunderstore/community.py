import mobase


class ThunderStoreCommunity:
    game_community_mapping = {
        # "valheim": "valheim",
        # "subnautica": "subnautica",
        "subnauticabelowzero": "subnautica-below-zero",
    }
    """Mapping MOs game short name (lowercase) to Thunderstore communities."""

    def get_community_name(self, game: mobase.IPluginGame):
        game_name = game.gameShortName().lower()
        return self.game_community_mapping.get(game_name, game_name)
