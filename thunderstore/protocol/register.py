import os
import shutil
import sys
import winreg
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

from .thunderstore_protocol import THUNDERSTORE_SCHEME


class ProtocolRegister:
    scheme: str
    command: str

    def __init__(self, scheme: str, command: str):
        self.scheme: str = scheme
        self.command: str = command

    def is_command_registered(self):
        """Check if the handler is registered in the registry."""
        return self.command == self.get_current_command()

    def get_current_command(self) -> str | None:
        """Get currently registered handler."""
        command_address = rf"Software\Classes\{self.scheme}\shell\open\command"
        try:
            with winreg.OpenKeyEx(
                winreg.HKEY_CURRENT_USER, command_address
            ) as command_key:
                return str(winreg.QueryValueEx(command_key, "")[0])
        except OSError:
            return None

    def register_protocol_command(self) -> tuple[str, str]:
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
                    self.command,
                )
        return rf"HKEY_CURRENT_USER\{classes_address}\shell\open\command", self.command


class ProtocolHandler(ABC):
    @abstractmethod
    def get_handler_command(self) -> str | None: ...


@dataclass
class PythonProtocolHandler(ProtocolHandler):
    mo_exe_path: Path
    python_exe: Path | None = None
    python_handler: Path = Path(__file__).parent

    def get_handler_command(self) -> str | None:
        python_exe = self.python_exe
        if not python_exe:
            python_exe = self.find_python_executable(self.mo_exe_path)
        if python_exe and (python_exe := python_exe.resolve()).exists():
            return f'"{python_exe}" "{os.path.abspath(self.python_handler)}" --gui --modorganizer "{self.mo_exe_path}"'
        return None

    def find_python_executable(
        self, mo_exe: str | Path | None = None, python_exe: str = "python3"
    ):
        if mo_exe:
            exe = Path(sys.executable)
            if exe.name != Path(mo_exe).name:
                return exe
        which = shutil.which(python_exe)
        return Path(which) if which else None


@dataclass
class ExeProtocolHandler(ProtocolHandler):
    mo_exe_path: Path
    compiled_handler: Path = Path(__file__, "../thunderstore_protocol_handler.exe")

    def get_handler_command(self) -> str | None:
        if (exe := Path(os.path.abspath(self.compiled_handler))).exists():
            if (exe_cmd := exe.with_suffix(".cmd")).exists():
                cmd = exe_cmd
            else:
                cmd = exe
            return f'"{cmd}" --gui --modorganizer "{self.mo_exe_path}"'
        return None


@dataclass
class ThunderstoreProtocolRegister(ProtocolRegister):
    mo_exe_path: Path
    python_exe: Path | None = None
    handlers: list[ProtocolHandler] = field(default_factory=list)
    reverse_order: bool = False
    scheme: str = THUNDERSTORE_SCHEME
    command: str = field(init=False)

    def __post_init__(self):
        if not self.handlers:
            self.handlers = [
                PythonProtocolHandler(self.mo_exe_path, self.python_exe),
                ExeProtocolHandler(self.mo_exe_path),
            ]
        super().__init__(self.scheme, self.get_handler_command())

    def get_handler_command(self):
        command = ""
        handlers = reversed(self.handlers) if self.reverse_order else self.handlers
        for handler in handlers:
            if command := handler.get_handler_command():
                break
        else:
            raise FileNotFoundError(
                "Cannot find protocol handler. Either install Python or compile the handler."
            )
        return f'{command} "%1"'
