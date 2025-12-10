"""Tests for xlsx server configuration."""

import os
from unittest.mock import patch

import pytest

from xlsx.server import DEFAULT_PORT, parse_args


class TestParseArgs:
    """Tests for parse_args function."""

    def test_defaults(self):
        """Test default argument values."""
        with patch("sys.argv", ["server.py"]):
            args = parse_args()
            assert args.transport == "stdio"
            assert args.host == "0.0.0.0"
            assert args.port == DEFAULT_PORT
            assert args.allow_origin == "*"

    def test_cli_arguments(self):
        """Test CLI arguments are parsed correctly."""
        with patch("sys.argv", ["server.py", "--transport", "sse", "--port", "9000", "--host", "127.0.0.1"]):
            args = parse_args()
            assert args.transport == "sse"
            assert args.port == 9000
            assert args.host == "127.0.0.1"

    def test_env_variables_as_defaults(self):
        """Test environment variables are used as defaults."""
        with patch.dict(os.environ, {"TRANSPORT": "sse", "PORT": "9999", "HOST": "localhost"}):
            with patch("sys.argv", ["server.py"]):
                args = parse_args()
                assert args.transport == "sse"
                assert args.port == 9999
                assert args.host == "localhost"

    def test_cli_overrides_env(self):
        """Test CLI arguments override environment variables."""
        with patch.dict(os.environ, {"TRANSPORT": "stdio", "PORT": "9999"}):
            with patch("sys.argv", ["server.py", "--transport", "sse", "--port", "8080"]):
                args = parse_args()
                assert args.transport == "sse"
                assert args.port == 8080

    def test_transport_choices(self):
        """Test transport argument only accepts valid choices."""
        with patch("sys.argv", ["server.py", "--transport", "invalid"]):
            with pytest.raises(SystemExit):
                parse_args()

    def test_allow_origin(self):
        """Test allow-origin argument."""
        with patch("sys.argv", ["server.py", "--allow-origin", "https://example.com"]):
            args = parse_args()
            assert args.allow_origin == "https://example.com"
