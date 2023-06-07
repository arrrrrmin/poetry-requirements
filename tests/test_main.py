import argparse
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from poetry_requirements import main


def test_error():
    e = main.Error(message="This is my error message!!!")
    assert e.message == "This is my error message!!!"
    with pytest.raises(main.Error, match="This is my error message!!!"):
        raise e


def test_check_poetry_version():
    v_strs = {
        "Poetry (version 1.2.0)": [1, 2, 0],
        "Poetry (version 1.1.14)": [1, 1, 14],
        "Poetry (version 1.2.0b3)": [1, 2, 0],
    }
    for v, res in v_strs.items():
        assert main.check_poetry_version(v) == res
    v = "Hello"
    with pytest.raises(main.Error, match="Poetry version unknown or not supported"):
        main.check_poetry_version(v)
    v = "1."
    with pytest.raises(
        main.Error,
        match="Only poetry versions 1.1.*/1.2.*/1.3.*/1.4.*/1.5.* are supported",
    ):
        main.check_poetry_version(v)


def test_poetry_argument_parser(capsys):
    parser, poetry_minor = main.poetry_argument_parser("Poetry (version 1.1.12)")
    parser.prog = ""
    usage_str = parser.format_usage()
    assert poetry_minor == 1
    assert isinstance(parser, argparse.ArgumentParser)
    assert all(
        argument in usage_str
        for argument in ["-o", "-E EXTRAS", "--without-hashes", "--dev"]
    )
    parser, poetry_minor = main.poetry_argument_parser("Poetry (version 1.2.0)")
    parser.prog = ""
    usage_str = parser.format_usage()
    assert poetry_minor == 2
    assert isinstance(parser, argparse.ArgumentParser)
    assert all(
        argument in usage_str
        for argument in (
            "-o",
            "-E EXTRAS",
            "--without-hashes",
            "--with WITH",
            "--without WITHOUT",
            "--only ONLY",
        )
    )
    with pytest.raises(main.Error, match="Poetry is not installed"):
        main.poetry_argument_parser("")


@patch("poetry_requirements.main.subprocess.check_output")
def __test_main_run(poetry_version_mock):
    mock_stdout = MagicMock()
    mock_stdout.configure_mock(**{"stdout.decode.return_value": ""})
    poetry_version_mock.return_value = b"Poetry (version 1.1.12)"
    main.run()


@patch("poetry_requirements.main.subprocess.check_output")
def test_exec_poetry_export(mock_poetry_export):

    mock_stdout = MagicMock()
    mock_stdout.configure_mock(**{"stdout.decode.return_value": ""})
    mock_poetry_export.return_value = b"poetry export output"

    params = {
        "o": "requirements.txt",
        "with": "dev",
        "extras": "lala more",
        "without_hashes": "--without_hashes",
    }
    arguments = argparse.Namespace(**params)
    output = main.exec_poetry_export(arguments, 2)

    assert output == "poetry export output"
    params = {
        "o": "requirements.txt",
        "dev": "--dev",
        "extras": "lala more",
        "without_hashes": "--without_hashes",
    }
    arguments = argparse.Namespace(**params)
    output = main.exec_poetry_export(arguments, 1)
    assert output == "poetry export output"


def test_read_existing_requirements():
    default_req_str = main.read_existing_requirements(Path("requirements.txt"))
    assert isinstance(default_req_str, str) and len(default_req_str) > 0
    assert main.read_existing_requirements(Path("fake/path/requirements.txt")) == ""


def test_update_requirements(tmpdir):
    requirements_path = Path(tmpdir) / "dependencies.txt"
    default_req_str = main.read_existing_requirements(Path("requirements.txt"))
    main.update_requirements(requirements_path, default_req_str)
    assert requirements_path.read_text() == default_req_str
