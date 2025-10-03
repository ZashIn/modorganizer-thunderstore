import json
import sys
from collections.abc import Sequence

import mobase

from .base import ThunderstoreBasePlugin
from .package_info import Manifest, PackageInfo


class ThunderstoreInstaller(ThunderstoreBasePlugin, mobase.IPluginInstallerSimple):
    """
    Installer for [thunderstore.io packages](https://thunderstore.io/package/create/docs/).
    Only extracts and sets mod metadata.

    The actual installation of mod contents is handled by other installers (with lower priority),
    like the Simple Installer (InstallerQuick), which uses `mobase.ModDataChecker`.
    """

    manifest_file = "manifest.json"
    package_files: list[str]

    def __init__(self) -> None:
        super().__init__()
        mobase.IPluginInstallerSimple.__init__(self)
        self.package_files = [
            self.manifest_file,
            "icon.png",
            "README.md",
            "CHANGELOG.md",
        ]

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._organizer.modList().onModInstalled(self.add_missing_url)
        return True

    def master(self) -> str:
        return self.base_name

    def name(self) -> str:
        return f"{self.base_name} Installer"

    def description(self) -> str:
        return f"{self.base_name} package installer"

    def settings(self) -> Sequence[mobase.PluginSetting]:
        return []

    def isArchiveSupported(self, tree: mobase.IFileTree) -> bool:
        manifest = tree.find(self.manifest_file, mobase.FileTreeEntry.FileTypes.FILE)
        return manifest is not None

    def isManualInstaller(self: mobase.IPluginInstaller) -> bool:
        return False

    def priority(self: mobase.IPluginInstaller) -> int:
        return 60

    def install(
        self,
        name: mobase.GuessedString,
        tree: mobase.IFileTree,
        version: str,
        nexus_id: int,
    ) -> (
        mobase.InstallResult
        | mobase.IFileTree
        | tuple[mobase.InstallResult, mobase.IFileTree, str, int]
    ):
        manifest_entry = tree.find(
            self.manifest_file, mobase.FileTreeEntry.FileTypes.FILE
        )
        if not manifest_entry or not (manifest := self.load_manifest(manifest_entry)):
            return mobase.InstallResult.NOT_ATTEMPTED
        name.update(manifest.name, mobase.GuessQuality.META)
        version = manifest.version_number
        # Return NOT_ATTEMPTED to let other installer, like Simple Installer (InstallerQuick), handle actual installation.
        return mobase.InstallResult.NOT_ATTEMPTED, tree, version, nexus_id

    def load_manifest(self, manifest_entry: mobase.FileTreeEntry):
        manifest_path = self._manager().extractFile(manifest_entry, silent=True)
        try:
            with open(manifest_path) as f:
                manifest = Manifest.from_json(json.load(f))
        except (json.JSONDecodeError, TypeError) as e:
            print(
                f"Decoding of {self.manifest_file} failed!",
                e,
                file=sys.stderr,
            )
            return None
        return manifest

    def add_missing_url(self, mod: mobase.IModInterface):
        if (
            mod.nexusId()
            or mod.isSeparator()
            or mod.isBackup()
            or mod.isForeign()
            or ((url := mod.url()) and not url.startswith(self.base_url))
            or not (community := self.get_community_name())
            or not (installation_file := mod.installationFile())
            or not (ts_mod_info := PackageInfo.from_file_path(installation_file))
        ):
            return
        url = ts_mod_info.get_url(self.base_url, community)
        mod_name = mod.name()
        print(f'Set missing URL for mod "{mod_name}":', url)
        mod.setUrl(url)
        mod_version = mod.version()
        if (
            not mod_version.isValid()
            or mod_version.scheme() == mobase.VersionScheme.DATE
        ):
            version = ts_mod_info.version
            print(f'Set missing version for mod "{mod_name}":', version)
            mod.setVersion(mobase.VersionInfo(version))
