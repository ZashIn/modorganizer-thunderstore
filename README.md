# Thunderstore support for Mod Organizer 2

Mod Organizer 2 plugin, adding [thunderstore.io](https://thunderstore.io/) website support.

## Features
- `ror2mm:` protocol handler for "Install with Mod Manager" links (registered on MO start or via tools menu)
- Thunderstore Installer (`IPluginInstaller`):
  - Set mod version and site link on mod installation (from package metadata).
  - Show missing dependencies (links).
  - Modify thunderstore package files (meta data), configurable via `package_file_action`.
  - Runs also on Nexus archive installations, since many authors include Thunderstore package metadata there, too.
- Thunderstore Mod Page (`IPluginModPage`):
  - Link to thunderstore community / game site (under 🌎).

## Installation
- Install/extract the `thunderstore` folder (from [Releases](https://github.com/ZashIn/modorganizer-thunderstore/releases)) into MO's plugins directory.

### Requirements
- Updated [basic_games plugins](https://github.com/ModOrganizer2/modorganizer-basic_games) for MO <2.5.2 Beta 3 (unreleased, see [PR](https://github.com/ModOrganizer2/modorganizer-basic_games/pull/199))
- For the `ror2mm:` protocol handler:
  - With installed Python 3.12+: the [Python script](thunderstore\protocol\cli.py) is used directly (source code / any MO version)
  - Without Python installed: `thunderstore/protocol/thunderstore_protocol_handler_python*.exe` is included in release, matching MOs Python version.

## Settings
Under `Setting/Plugins/Thunderstore`:
- `thunderstore_community`: by default set by the game plugin (see [Add game support](#add-game-support) below).

`Thunderstore Installer`:
- `check_dependencies`: display missing dependencies (default: true).
- `package_file_action`: ignore, remove or hide (default, adds `.mohidden` suffix).

## Development info
### Protocol handler compilation
To support Windows systems without a Python installation, a compiled Python handler (`thunderstore/protocol/cli.py`) is also included, using MOs bundled `plugin_python` libs.

Building `thunderstore/protocol/thunderstore_protocol_handler.exe`:
- install [Nuitka requirements](https://nuitka.net/user-documentation/user-manual.html#requirements)
- install [Poetry](https://python-poetry.org/docs/#installation), e.g. via `pipx install poetry`
- `poetry install --no-root --with build`: including optional build deps
- `poe build`: for small exe, using MOs integrated Python libs (`plugins/plugin_python/dlls`), **Python version has to match**
- `poe build-standalone`: for standalone exe with integrated python.

### Add game support
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

The games `ModDataChecker` / `IPluginInstaller` should be configured together with the `package_file_action`, e.g.
```py
# Hide the Thunderstore package files (default)
#organizer.setPluginSetting("Thunderstore Installer", "package_file_action", "hide")
BasicModDataChecker(GlobPatterns(ignore=["*.mohidden"]))
# Remove them
organizer.setPluginSetting("Thunderstore Installer", "package_file_action", "remove")
```

## Limitations
Current [Mod Organizer API limitations](https://github.com/ModOrganizer2/modorganizer/issues/2286):
- Cannot show thunderstore website in MOs internal browser (only Nexus supported / does not handle downloads correctly)