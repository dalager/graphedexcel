import pytest
import sys

# from argparse import Namespace
from graphedexcel.cli import parse_arguments, main
from unittest.mock import patch, MagicMock


def test_parse_arguments_required(monkeypatch):
    """
    Test that the required positional argument is parsed correctly.
    """
    test_args = ["graphedexcel", "test.xlsx"]
    with patch("sys.argv", test_args):
        args = parse_arguments()
        assert args.path_to_excel == "test.xlsx"


def test_parse_arguments_optional_flags():
    """
    Test that optional flags are parsed correctly.
    """
    test_args = ["graphedexcel", "test.xlsx", "--as-directed-graph", "--no-visualize"]
    with patch("sys.argv", test_args):
        args = parse_arguments()
        assert args.path_to_excel == "test.xlsx"
        assert args.as_directed_graph is True
        assert args.no_visualize is True


def test_parse_arguments_optional_arguments():
    """
    Test that optional arguments are parsed correctly.
    """
    test_args = [
        "graphedexcel",
        "test.xlsx",
        "--layout",
        "circular",
        "--config",
        "config.json",
        "--output-path",
        "output.png",
        "--open-image",
    ]
    with patch("sys.argv", test_args):
        args = parse_arguments()
        assert args.path_to_excel == "test.xlsx"
        assert args.layout == "circular"
        assert args.config == "config.json"
        assert args.output_path == "output.png"
        assert args.open_image is True


def test_parse_arguments_default_values():
    """
    Test that default values are set correctly.
    """
    test_args = ["graphedexcel", "test.xlsx"]
    with patch("sys.argv", test_args):
        args = parse_arguments()
        assert args.layout == "spring"
        assert args.config is None
        assert args.output_path is None
        assert args.as_directed_graph is False
        assert args.no_visualize is False
        assert args.open_image is False


def test_parse_arguments_invalid():
    """
    Test that invalid arguments raise a SystemExit.
    """
    test_args = ["graphedexcel"]
    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit):
            parse_arguments()
