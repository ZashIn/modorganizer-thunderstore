# Thunderstore support for Mod Organizer 2

Mod Organizer 2 plugin, adding [thunderstore.io](thunderstore.io) website support.

## Features
- Adds an `IPluginModPage` for thunderstore
- Link to thunderstore community / game site
- Set mod version and mod site link on mod installation (from file info)

## Installation
Install the `thunderstore` module folder into MO's plugins directory.

## Dev info: add game support
You can add thunderstore support to a game plugin ([`BasicGame`](https://github.com/ModOrganizer2/modorganizer-basic_games) / [IPluginGame](https://www.modorganizer.org/python-plugins-doc/plugin-types.html#game)) by setting the community name in one of the following ways:
- Add a [setting](https://www.modorganizer.org/python-plugins-doc/autoapi/mobase/index.html#mobase.PluginSetting) `"thunderstore_community"` to a game plugin:
  ```py
  mobase.PluginSetting("thunderstore_community", "Thunderstore community name", "<community_name>")
  ```
- Add a `GameThunderstoreName` attribute or `gameThunderstoreName()` method to the game plugin.
- Set the setting `"thunderstore_community"` of this plugin to the game community name  from another plugin via:
  ```py
  organizer.setPluginSetting("Thunderstore" or game.name(), "thunderstore_community", "<community_name>")
  ```
- Set the setting **manually** in MO under `Settings/Plugins/Plugin/Thunderstore/thunderstore_community` (and restart MO).

## Limitations
Current [Mod Organizer API limitations](https://github.com/ModOrganizer2/modorganizer/issues/2286):
- Direct download/install ("Install with Mod Manager") via `ror2mm://` protocol not supported.  
  **Alternative:** Manual download into the MOs instance download folder adds it to the download list
- Cannot show thunderstore website in MOs internal browser (only Nexus supported / does not handle downloads correctly)