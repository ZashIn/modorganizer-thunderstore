import argparse
import re
import subprocess
import sys

PLUGIN_FILE_WITH_VERSION = "thunderstore/base.py"
PROJECT_FILE = "pyproject.toml"

parser = argparse.ArgumentParser(
    description="Update pyproject.toml and plugin version."
)
parser.add_argument("version", nargs="?", default="", help="See: poetry version --help")
parser.add_argument(
    "-p",
    "--plugin",
    default=PLUGIN_FILE_WITH_VERSION,
    help="Path to the plugin py file with mobase.Version, default: %(default)s",
)
parser.add_argument("-s", "--stage", action="store_true", help="Stage changes with git")


def update_plugin_version(plugin_version_file: str, new_version: str = ""):
    with open(plugin_version_file) as f:
        text = f.read()
    if not (
        match := re.search(
            r"(VersionInfo\(\s*)(?P<version>\d+\s*,\s*\d+\s*,\s*\d+)(?P<rest>(?:\s*,\s*(?P<releaseType>[^)\s]+))?\))",
            text,
        )
    ):
        raise ValueError(f"VersionInfo not found in file {plugin_version_file}!")
    package_version = poetry_version(new_version)
    plugin_version = re.sub(r"\s*,\s*", ".", match["version"])
    if package_version != plugin_version:
        text = "".join(
            [
                text[: match.start()],
                match[1],
                ", ".join(package_version.split(".")),
                match["rest"],
                text[match.end() :],
            ]
        )
        with open(plugin_version_file, "w") as f:
            f.write(text)
        print(
            f"Version updated in {PROJECT_FILE} and {plugin_version_file}: {plugin_version} -> {package_version}"
        )
        return True
    else:
        print(
            f"Current version in {PROJECT_FILE} and {plugin_version_file}: {package_version}"
        )
        return False


def poetry_version(new_version: str = ""):
    res: subprocess.CompletedProcess[str] = subprocess.run(
        f"poetry version -s {new_version}", shell=True, capture_output=True, text=True
    )
    if not res.stdout:
        raise ValueError("poetry version output invalid!")
    return res.stdout.strip()


def main(sys_args: list[str] = sys.argv[1:]):
    args = parser.parse_args(sys_args)
    pending = (
        re.search(
            "|".join([re.escape(PROJECT_FILE), re.escape(args.plugin)]),
            subprocess.run(
                "git status -s", shell=True, capture_output=True, text=True
            ).stdout,
        )
        if args.stage
        else True
    )
    if update_plugin_version(args.plugin, args.version) and not pending:
        subprocess.run(
            f'git add -- "{args.plugin}" "{PROJECT_FILE}"',
            shell=True,
        )


if __name__ == "__main__":
    main()
