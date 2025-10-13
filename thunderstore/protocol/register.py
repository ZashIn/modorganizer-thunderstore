#!/usr/bin/env python3
import shutil
import sys
import winreg
from dataclasses import dataclass
from pathlib import Path

from .thunderstore_protocol import THUNDERSTORE_SCHEME

HANDLER = Path(__file__).parent.absolute()


def get_python_executable(mo_executable: str | Path | None = None):
    if mo_executable:
        exe = Path(sys.executable)
        if exe.name != Path(mo_executable).name:
            return exe
    return shutil.which("python3")


@dataclass
class ProtocolRegister:
    mo_exe_path: str | Path
    scheme: str = THUNDERSTORE_SCHEME
    python_path: Path | None = None

    def register_protocol_handler(
        self,
    ) -> tuple[str, str]:
        """
        Returns:
            (key_address, command)
        """
        return self.register_protocol_command(self.get_handler_command())

    def get_handler_command(self):
        python_path = self.python_path or get_python_executable(self.mo_exe_path)
        assert python_path
        python_path = Path(python_path).resolve()
        return f'{python_path} "{HANDLER}" -m "{self.mo_exe_path}" "%1"'

    def is_handler_registered(
        self,
    ):
        """Check if the handler is registered in the registry."""
        command = self.get_handler_command()
        registered_handler = self.get_current_handler()
        return command == registered_handler

    def get_current_handler(self) -> str | None:
        """Get currently registered handler."""
        command_address = rf"Software\Classes\{self.scheme}\shell\open\command"
        try:
            with winreg.OpenKeyEx(
                winreg.HKEY_CURRENT_USER, command_address
            ) as command_key:
                return str(winreg.QueryValueEx(command_key, "")[0])
        except OSError:
            return None

    def register_protocol_command(self, command: str) -> tuple[str, str]:
        """
        Register a handler command for the protocol in the registry.

        Returns:
            (key_address, command)
        """
        classes_address = rf"Software\Classes\{self.scheme}"
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, classes_address) as th_scheme:
            winreg.SetValueEx(
                th_scheme,
                None,
                0,
                winreg.REG_SZ,
                f"URL:{self.scheme.upper()} Protocol",
            )
            winreg.SetValueEx(th_scheme, "URL Protocol", 0, winreg.REG_SZ, None)
            with winreg.CreateKeyEx(th_scheme, r"shell\open\command") as command_key:
                winreg.SetValueEx(
                    command_key,
                    None,
                    0,
                    winreg.REG_SZ,
                    command,
                )
        return rf"HKEY_CURRENT_USER\{classes_address}\shell\open\command", command
