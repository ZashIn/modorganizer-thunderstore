import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any, override

import mobase
from PyQt6.QtCore import qInfo
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QCheckBox, QMainWindow, QMessageBox, QWidget

from .base import ThunderstoreBasePlugin
from .protocol.register import ThunderstoreProtocolRegister
from .protocol.utils import abs_norm_path


class ThunderstoreRegisterTool(ThunderstoreBasePlugin, mobase.IPluginTool):
    def __init__(self) -> None:
        super().__init__()
        mobase.IPluginTool.__init__(self)

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self.protocol_register = ThunderstoreProtocolRegister(
            abs_norm_path(sys.executable)
        )
        if self._organizer.pluginSetting(self.name(), "register_protocol"):
            if self.protocol_register.is_command_registered():
                self._organizer.setPluginSetting(
                    self.name(), "register_protocol", False
                )
                return True

            def callback(win: QMainWindow):
                dialog = RegisterProtocolDialog(
                    self.protocol_register, win
                ).with_do_not_show_again_checkbox(
                    lambda checked: self._organizer.setPluginSetting(
                        self.name(), "register_protocol", not checked
                    ),
                    f"Settings/Plugins/{self.master()}/{self.name()}/register_protocol",
                )
                dialog.open()

            organizer.onUserInterfaceInitialized(callback)
        return True

    def settings(self) -> Sequence[mobase.PluginSetting]:
        return [
            mobase.PluginSetting(
                "register_protocol",
                "Show a dialog to register the Thunderstore ror2mm: protocol",
                True,
            )
        ]

    def master(self) -> str:
        return self.base_name

    def name(self) -> str:
        return f"{self.base_name}/Register Protocol"

    def displayName(self) -> str:
        return self.name()

    def tooltip(self) -> str:
        return f'Open "Install with Mod Manager" links ({ThunderstoreProtocolRegister.scheme}:) with Mod Organizer'

    def icon(self) -> QIcon:
        return QIcon(
            str(abs_norm_path(Path(__file__).with_name("thunderstore_icon.png")))
        )

    def display(self) -> None:
        if self.protocol_register.is_command_registered():
            QMessageBox.information(
                self._parentWidget(),
                f"Protocol {self.protocol_register.scheme}: registered",
                f"MO is already registered as handler for {self.protocol_register.scheme}://.",
            )
            return
        dialog = RegisterProtocolDialog(self.protocol_register, self._parentWidget())
        dialog.open()


class RegisterProtocolDialog(QMessageBox):
    protocol_register: ThunderstoreProtocolRegister
    do_not_show_again_callback: Callable[[bool], Any] | None = None

    @override
    def __init__(
        self,
        protocol_register: ThunderstoreProtocolRegister,
        parent: QWidget | None = None,
    ):
        self.protocol_register = protocol_register
        super().__init__(
            QMessageBox.Icon.Question,
            f"Register {protocol_register.scheme}: Protocol",
            f'Do you want associate "Install with Mod Manager" links ({protocol_register.scheme}://) with Mod Organizer?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            parent=parent,
        )
        self.accepted.connect(self.register_protocol)

    def with_do_not_show_again_checkbox(
        self, callback: Callable[[bool], Any], tooltip: str = ""
    ):
        self.do_not_show_again_callback = callback
        checkbox = QCheckBox("Do not show again", self)
        checkbox.setChecked(True)
        if tooltip:
            checkbox.setToolTip(tooltip)
        self.setCheckBox(checkbox)
        self.finished.connect(
            lambda _: self.do_not_show_again_callback
            and self.do_not_show_again_callback(checkbox.isChecked())
        )
        return self

    def register_protocol(self):
        key, command = self.protocol_register.register_protocol_command()
        qInfo(
            f"Protocol {self.protocol_register.scheme}: registered under {key} as: {command}"
        )
