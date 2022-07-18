import argparse
import subprocess
from typing import Sequence
from pathlib import Path


class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, *, message: str):
        self.message = message
        super().__init__(self.message)


requirments_txt_missing_error = Error(message="File requirements.txt is missing")
poetry_not_installed_error = Error(message="Poetry is not installed")
poetry_export_error = Error(
    message="Unable to execute `poetry export`, check `args` in your `.pre-commit-hooks.yaml`"
)
requirements_txt_outdated = Error(message="Requirements.txt needs update")


def requirements_txt_exist(path_string: str) -> bool:
    """Check if requirements.txt file exists"""
    return Path(path_string).exists()


def poetry_exists() -> bool:
    """Check if poetry exists by prompting it"s version"""
    version_string = subprocess.check_output(["poetry", "--version"])
    return "Poetry version " in version_string.decode("utf-8")


def exec_poetry_export(args: argparse.Namespace) -> (str | Error):
    """Execute poetry export and generate a requirements.txt"""
    cmd = ["poetry", "export"]
    if args.extras:
        cmd += f"--extras {args.extras}".split()
    if args.dev:
        cmd += [args.dev]
    if args.without_hashes:
        cmd += [args.without_hashes]
    if args.with_credentials:
        cmd += [args.with_credentials]
    print(
        f"Command for poetry export based on args in `.pre-commit-hooks.yaml`: {' '.join(cmd)}"
    )
    try:
        current_requirements_string = subprocess.check_output(cmd).decode("utf-8")
    except Exception:
        raise poetry_export_error
    return current_requirements_string


def read_existing_requirements(requirements_path: Path) -> (str | Error):
    """If existing read requirements.txt file"""
    if not requirements_path.exists():
        print(f"File `{requirements_path}` does not exist")
        return ""
    return requirements_path.read_text(encoding="utf-8")


def update_requirements(
    *, requirements_path: Path, updated_requirements: str
) -> (Path | Error):
    """Write a new requirements.txt file with current environment dependencies"""
    requirements_path.write_text(updated_requirements, encoding="utf-8")
    return requirements_path


def run(argv: Sequence[str] | None = None) -> int:
    """Runs the hook with arguments from users `.pre-commit-hooks.yaml`"""
    parser = argparse.ArgumentParser()
    # parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        default="requirements.txt",
        type=str,
        help="The name of the output file. If omitted, print to standard output",
    )
    parser.add_argument(
        "-E",
        "--extras",
        dest="extras",
        action="extend",
        nargs="+",
        type=str,
        help="Extra sets of dependencies to include",
    )
    parser.add_argument(
        "--dev",
        dest="dev",
        action="store_const",
        const="--dev",
        help="Include development dependencies",
    )
    parser.add_argument(
        "--without-hashes",
        dest="without_hashes",
        action="store_const",
        const="--without-hashes",
        help="Exclude hashes from the exported file",
    )
    parser.add_argument(
        "--with-credentials",
        dest="with_credentials",
        action="store_const",
        const="--with-credentials",
        help="Include credentials for extra indices",
    )
    retv = 0
    if not poetry_exists():
        retv = 1
        print(poetry_not_installed_error.message)
    arguments = parser.parse_args(argv)
    requirements_txt = Path("./").joinpath(arguments.output)
    actual_requirements = exec_poetry_export(args=arguments)
    existing_requirements = read_existing_requirements(requirements_path=requirements_txt)
    if retv == 0 and not actual_requirements == existing_requirements:
        print("Requirements don't match poetry envionment, exporting dependencies ...")
        updated_file = update_requirements(
            requirements_path=requirements_txt, updated_requirements=actual_requirements
        )
        print(f"Updated {updated_file}")
        retv = 1
    return retv


if __name__ == "__main__":
    raise SystemExit(run())
