import json
import sys
from collections.abc import Callable, Iterable, Sequence

import mobase
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from .base import ThunderstoreBasePlugin
from .package_info import Manifest, PackageInfo
from .utils import hide_file_tree_entry


class ThunderstoreInstaller(ThunderstoreBasePlugin, mobase.IPluginInstallerSimple):
    """
    Installer for [thunderstore.io packages](https://thunderstore.io/package/create/docs/).
    Only extracts mod metadata and modifies metadata package files (according to setting `package_file_action`).

    The actual installation of mod contents is handled by other installers (with lower priority),
    like the Simple Installer (InstallerQuick), which uses `mobase.ModDataChecker`.
    """

    package_file_actions: dict[
        str, Callable[[mobase.IFileTree, mobase.FileTreeEntry], bool]
    ]
    """
    Callback for each file in `.package_files`. The action is chosen by the setting `package_file_action`.
    Return False to abort the file iteration.
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
        self.package_file_actions = {
            "ignore": lambda tree, entry: False,
            "hide": hide_file_tree_entry,
            "remove": lambda tree, entry: entry.detach(),
        }

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
        return [
            mobase.PluginSetting(
                "check_dependencies",
                "Check dependencies from thunderstore manifest",
                True,
            ),
            mobase.PluginSetting(
                "package_file_action",
                f"What to do with package files: {', '.join(self.package_file_actions)}",
                "hide",
            ),
        ]

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
        # Update metadata
        name.update(manifest.name, mobase.GuessQuality.META)
        version = manifest.version_number
        # Check dependencies
        if manifest.dependencies and not self.check_dependencies(
            manifest.dependencies, manifest.name
        ):
            return mobase.InstallResult.CANCELED
        # Modify package files
        if (action := self.get_package_file_action()) is not None:
            for file in self.package_files:
                if (entry := tree.find(file)) is not None and not action(tree, entry):
                    break
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

    def check_dependencies(self, dependencies: Iterable[str], mod_name: str):
        if self._organizer.pluginSetting(self.name(), "check_dependencies") is False:
            return True
        modlist = self._organizer.modList()
        installed_deps: list[str] = []
        missing_deps: list[PackageInfo | str] = []
        for dep_str in dependencies:
            if not (ts_mod_info := PackageInfo.parse_dependency_str(dep_str)):
                print(f"Unknown dependency: {dep_str}", file=sys.stderr)
            if mod := (
                ts_mod_info
                and (
                    modlist.getMod(ts_mod_info.name)
                    or modlist.getMod(ts_mod_info.full_name)
                )
                or modlist.getMod(dep_str)
            ):
                installed_deps.append(mod.name())
            else:
                missing_deps.append(ts_mod_info or dep_str)
        if missing_deps:
            community = self.get_community_name()
            missing_deps_md = (
                f"[{d.dependency_str}]({d.get_url(self.base_url, community)})"
                if isinstance(d, PackageInfo)
                else d
                for d in missing_deps
            )
            installed = (
                f"\n\nInstalled:\n- {'\n- '.join(installed_deps)}"
                if installed_deps
                else ""
            )
            msg = QMessageBox(
                QMessageBox.Icon.Information,
                "Missing dependencies",
                (
                    f'For the mod "{mod_name}" the following dependencies are required:\n\n'
                    f"Missing:\n- {'\n- '.join(missing_deps_md)}"
                    f"{installed}"
                ),
                buttons=QMessageBox.StandardButton.Ok
                | QMessageBox.StandardButton.Cancel,
                parent=self._parentWidget(),
            )
            msg.setTextFormat(Qt.TextFormat.MarkdownText)
            return msg.exec() != QMessageBox.StandardButton.Cancel
        return True

    def get_package_file_action(self):
        if action_name := self._organizer.pluginSetting(
            self.name(), "package_file_action"
        ):
            return self.package_file_actions.get(str(action_name), None)
        return None

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
