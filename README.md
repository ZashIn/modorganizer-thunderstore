# Thunderstore support for Mod Organizer 2

Mod Organizer 2 plugin, adding [thunderstore.io](thunderstore.io) website support.

## Features
- Adds an `IPluginModPage` for thunderstore
- Link to thunderstore community / game site
- Set mod version and mod site link on mod installation (from file info)

## Limitations
Current [Mod Organizer API limitations](https://github.com/ModOrganizer2/modorganizer/issues/2286):
- Direct download/install ("Install with Mod Manager") via `ror2mm://` protocol not supported.  
  **Alternative:** Manual download into the MOs instance download folder adds it to the download list
- Cannot show thunderstore website in MOs internal browser (only Nexus supported / does not handle downloads correctly)