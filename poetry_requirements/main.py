import argparse
import re
import subprocess
from typing import Sequence, List, Tuple
from pathlib import Path


class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, *, message: str):
        self.message = message
        super().__init__(self.message)


requirements_txt_missing_error = Error(message="File requirements.txt is missing")
poetry_not_installed_error = Error(message="Poetry is not installed")
poetry_export_error = Error(
    message="Unable to execute `poetry export`, check `args` in your `.pre-commit-hooks.yaml`"
)
requirements_txt_outdated = Error(message="Requirements.txt needs update")
v_pat = re.compile(r"([\d.]+)")
supported_minors = ("1", "2")


def check_poetry_version(v: str) -> List[int]:
    """Check and return the version ints from version string"""
    pat_findings = v_pat.findall(v)
    if not len(pat_findings) >= 1:
        raise Error(message="Poetry version unknown or not supported")  # Todo
    if pat_findings[0].split(".")[1] not in supported_minors:
        raise Error(message="Only poetry versions 1.1.*/1.2.* are supported")  # Todo
    return [int(v_sub_str) for v_sub_str in pat_findings[0].split(".")]


def poetry_argument_parser(v: str) -> (Tuple[argparse.ArgumentParser, int] | Error):
    if not all(i in v for i in ("Poetry", "version")):
        raise poetry_not_installed_error
    version = check_poetry_version(v)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", dest="output", default="requirements.txt", type=str
    )
    parser.add_argument(
        "-E", "--extras", dest="extras", action="extend", nargs="+", type=str
    )
    parser.add_argument(
        "--without-hashes", action="store_const", const="--without-hashes"
    )
    if version[1] == 2:
        parser.add_argument("--without", action="extend", nargs="+", type=str)
        parser.add_argument("--with", action="extend", nargs="+", type=str)
        parser.add_argument("--only", action="extend", nargs="+", type=str)
    if version[1] == 1:
        parser.add_argument("--dev", dest="dev", action="store_const", const="--dev")
    poetry_minor_version = version[1]
    return parser, poetry_minor_version


def exec_poetry_export(
    args: argparse.Namespace, poetry_minor_version: int
) -> (str | Exception):
    """Execute poetry export and generate a requirements.txt"""
    cmd = ["poetry", "export"]
    if args.extras:
        cmd += f"--extras {args.extras}".split()
    if poetry_minor_version == 1:
        if args.dev:
            cmd += [args.dev]
    if poetry_minor_version == 2:
        if args.__dict__["with"]:
            cmd += f"--with {args.__dict__['with']}".split()
    if args.without_hashes:
        cmd += [args.without_hashes]
    print(
        f"Command for poetry export based on args in `.pre-commit-hooks.yaml`: {' '.join(cmd)}"
    )
    current_requirements_string = subprocess.check_output(cmd).decode("utf-8")
    return current_requirements_string


def read_existing_requirements(requirements_path: Path) -> (str | Error):
    """If existing read requirements.txt file"""
    if not requirements_path.exists():
        print(f"File `{requirements_path}` does not exist")
        return ""
    return requirements_path.read_text(encoding="utf-8")


def update_requirements(
    requirements_path: Path, updated_requirements: str
) -> (Path | Error):
    """Write a new requirements.txt file with current environment dependencies"""
    requirements_path.write_text(updated_requirements, encoding="utf-8")
    return requirements_path


def run(argv: Sequence[str] | None = None) -> int:  # pragma no cover
    """Runs the hook with arguments from users `.pre-commit-hooks.yaml`"""
    # Todo find a good way to test this
    v = subprocess.check_output(["poetry", "--version"]).decode("utf-8").strip()
    parser, poetry_minor = poetry_argument_parser(v)
    return_val = 0
    arguments = parser.parse_args(argv)
    requirements_txt = Path("./").joinpath(arguments.output)
    actual_requirements = exec_poetry_export(arguments, poetry_minor)
    existing_requirements = read_existing_requirements(requirements_txt)
    if return_val == 0 and not actual_requirements == existing_requirements:
        print("Requirements don't match poetry environment, exporting dependencies ...")
        updated_file = update_requirements(
            requirements_path=requirements_txt, updated_requirements=actual_requirements
        )
        print(f"Updated {updated_file}")
        return_val = 1
    return return_val


if __name__ == "__main__":
    raise SystemExit(run())
