# Changelog

## 0.3.0
Add `ror2mm:` protocol handler for "Install with Mod Manager" links, registered on MO start or via tools menu.

## 0.2.1
Adds a Thunderstore Installer (`IPluginInstaller`):
- Set mod version and site link on mod installation (from package metadata and file name).
- Show missing dependencies (links).
- Modify thunderstore package files (meta data), configurable via `package_file_action`.
### Settings
- `thunderstore_community`: by default set by the game plugin (see below).
- `check_dependencies`: display missing dependencies (default: true).
- `package_file_action`: ignore, remove or hide (default, adds `.mohidden` suffix).

## 0.1.0
Adds a Thunderstore Mod Page (`IPluginModPage`):
- Link to thunderstore community / game site (under 🌎).
- Set mod version and mod site link on mod installation (from file info)