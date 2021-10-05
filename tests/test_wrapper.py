import unittest.mock

import pytest
from click.testing import CliRunner

from stable_po_pre_commit.cli import main


@pytest.fixture
def mocked_babel():
    with unittest.mock.patch("stable_po_pre_commit.cli.CommandLineInterface") as cli:
        yield cli


@pytest.fixture
def runner():
    return CliRunner()


def test_no_arguments(mocked_babel, runner):
    result = runner.invoke(main, [])

    mocked_calls = mocked_babel.return_value.run.mock_calls
    assert len(mocked_calls) == 1

    called_args = mocked_calls[0].args[0]
    assert called_args == [
        "pybabel",
        "extract",
        "--no-location",
        "--omit-header",
        "--no-wrap",
        "--sort-output",
        "-k",
        "lazy_gettext",
        "-c",
        "BABEL:",
    ]
    assert result.exit_code == 0


def test_files_passed_through(mocked_babel, runner):
    result = runner.invoke(main, ["a", "b", "c"])

    mocked_calls = mocked_babel.return_value.run.mock_calls
    assert len(mocked_calls) == 1

    called_args = mocked_calls[0].args[0]
    assert called_args == [
        "pybabel",
        "extract",
        "--no-location",
        "--omit-header",
        "--no-wrap",
        "--sort-output",
        "-k",
        "lazy_gettext",
        "-c",
        "BABEL:",
        "a",
        "b",
        "c",
    ]
    assert result.exit_code == 0


def test_output_location_passed(mocked_babel, runner):
    result = runner.invoke(main, ["-o", "output"])

    mocked_calls = mocked_babel.return_value.run.mock_calls
    assert len(mocked_calls) == 2

    called_args = mocked_calls[0].args[0]
    assert called_args == [
        "pybabel",
        "extract",
        "--no-location",
        "--omit-header",
        "--no-wrap",
        "--sort-output",
        "-k",
        "lazy_gettext",
        "-c",
        "BABEL:",
        "-o",
        "output",
    ]

    called_args = mocked_calls[1].args[0]
    assert called_args == ['pybabel',
 'update',
 '--ignore-obsolete',
 '--omit-header',
 '--no-wrap',
 '--no-fuzzy-matching',
 '-i',
 'output',
 '-d',
 '/pool/rps/stable_po_pre_commit/tests/translations']

    assert result.exit_code == 0


def test_mapping_file_passed(mocked_babel, runner):
    result = runner.invoke(main, ["-F", "mapping"])


    mocked_calls = mocked_babel.return_value.run.mock_calls
    assert len(mocked_calls) == 1

    called_args = mocked_calls[0].args[0]
    assert called_args == [
        "pybabel",
        "extract",
        "--no-location",
        "--omit-header",
        "--no-wrap",
        "--sort-output",
        "-k",
        "lazy_gettext",
        "-c",
        "BABEL:",
        "-F",
        "mapping",
    ]
    assert result.exit_code == 0
