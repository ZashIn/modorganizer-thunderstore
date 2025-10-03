# Thunderstore support for Mod Organizer 2

Mod Organizer 2 plugin, adding [thunderstore.io](https://thunderstore.io/) website support.

## Features
- Adds a Thunderstore Installer (`IPluginInstaller`):
  - Set mod version and site link on mod installation (from package metadata).
  - Show missing dependencies (links).
  - Modify thunderstore package files (meta data), configurable via `package_file_action`.
- Adds a Thunderstore Mod Page (`IPluginModPage`):
  - Link to thunderstore community / game site (under 🌎).

## Installation
Install the `thunderstore` module folder into MO's plugins directory.

## Usage
1. On [thunderstore.io](https://thunderstore.io/) (can be opened in MO from 🌎) download a mod via Manual Download:
  Either download directly into MOs downloads dir (in MO: 📁▾ Open Downloads folder)  
  or via drag & drop (link or downloaded file) into MOs downloads tab.
1. (Refresh downloads in MO.)
2. Double click the download in MO (or right click / Install).
3. Thunderstore link and version is updated, package metadata files are installed hidden (by default) from MOs virtual file system.

## Settings
Under `Setting/Plugins/Thunderstore`:
- `thunderstore_community`: by default set by the game plugin (see below).

`Thunderstore Installer`:
- `check_dependencies`: display missing dependencies (default: true).
- `package_file_action`: ignore, remove or hide (default, adds `.mohidden` suffix).

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