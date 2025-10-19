#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from collections.abc import Callable
from functools import partial
from pathlib import Path
from tkinter import messagebox
from typing import Any
from urllib.request import urlopen

from .register import ThunderstoreProtocolRegister
from .thunderstore_protocol import ThunderstoreProtocol
from .utils import abs_norm_path

MO_EXE = "ModOrganizer.exe"


def get_mo_executable() -> Path:
    # MO (MO_EXE)/plugins/thunderstore/protocol/__file__
    return abs_norm_path(os.path.join(__file__, "../../../..", MO_EXE))


parser = argparse.ArgumentParser(
    description=(
        f"{ThunderstoreProtocol.scheme}: protocol handler for Mod Organizer. Required: -r/--register or url"
    )
)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "url",
    default="",
    nargs="?",
    help=f"URL to download, following {ThunderstoreProtocol.url_base}...",
)
group.add_argument(
    "-r",
    "--register",
    action="store_true",
    help=f"register as {ThunderstoreProtocol.scheme}: handler",
)
parser.add_argument(
    "-e", "--exe", help="prefer compiled exe over python handler", action="store_true"
)
parser.add_argument(
    "-m",
    "--modorganizer",
    help=f"path to {MO_EXE} (defaults to .../plugins/../{MO_EXE})",
    type=Path,
    default=None,
)
parser.add_argument(
    "-s",
    "--silent",
    help="Suppress non-error messages.",
    action="store_true",
)
parser.add_argument(
    "-g",
    "--gui",
    dest="gui",
    help="output errors in GUI / messagebox instead of CLI.",
    action="store_true",
)


def mo_download_command(mo_executable: str | Path, url: str):
    return [mo_executable, "download", url]


def download_with_mo(mo_executable: str | Path, url: str):
    subprocess.Popen(mo_download_command(mo_executable, url))


def resolve_redirections(url: str):
    """Workaround for [BUG: MO not resolving download URL redirections](https://github.com/ModOrganizer2/modorganizer/issues/2298)."""
    with urlopen(url) as response:
        return response.geturl()


class Output:
    info: Callable[..., Any]
    error: Callable[..., Any]

    def __init__(
        self, gui: bool = False, title: str = "", silent: bool = False
    ) -> None:
        self.info = (lambda *args: None) if silent else print
        if gui:
            self.error = lambda *args: messagebox.showerror(
                title, " ".join(str(a) for a in args)
            )
        else:
            self.error = partial(print, file=sys.stderr)


def main():
    args = parser.parse_args()
    out = Output(
        args.gui or sys.stderr is None,
        f"{ThunderstoreProtocol.scheme}:// handler for Mod Organizer",
        args.silent,
    )
    mo_exe_path: Path | None = args.modorganizer or get_mo_executable()
    if mo_exe_path and mo_exe_path.is_dir():
        mo_exe_path = mo_exe_path / MO_EXE
    if not mo_exe_path or not mo_exe_path.exists():
        out.error("Mod Organizer executable not found:", mo_exe_path)
        return 1
    if args.register:
        protocol_register = ThunderstoreProtocolRegister(
            mo_exe_path, reverse_order=args.exe
        )
        reg_address, command = protocol_register.register_protocol_command()
        out.info(f'Protocol registered under "{reg_address}" as:', command)
        return 0
    try:
        dl_url = ThunderstoreProtocol.parse_url(args.url).get_download_url()
    except ValueError as e:
        # Invalid protocol
        out.error(e)
        return 2
    if dl_url:
        out.info("Resolving redirections for:", dl_url)
        dl_url = resolve_redirections(dl_url)
        out.info("Running:", *mo_download_command(mo_exe_path, dl_url))
        download_with_mo(
            mo_exe_path,
            dl_url,
        )
    return 0


if __name__ == "__main__":
    if (exit_code := main()) > 0:
        sys.exit(exit_code)
