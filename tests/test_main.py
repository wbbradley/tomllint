"""Tests for tomllint."""

import subprocess
import sys
from pathlib import Path

import pytest

TOMLLINT_CMD = [sys.executable, "-m", "tomllint.main"]


@pytest.fixture
def valid_toml(tmp_path: Path) -> Path:
    """Create a temporary valid TOML file."""
    f = tmp_path / "valid.toml"
    f.write_text('[section]\nkey = "value"\nnumber = 42\n')
    return f


@pytest.fixture
def invalid_toml(tmp_path: Path) -> Path:
    """Create a temporary invalid TOML file."""
    f = tmp_path / "invalid.toml"
    f.write_text('key = "unclosed string\n')
    return f


@pytest.fixture
def another_valid_toml(tmp_path: Path) -> Path:
    """Create another temporary valid TOML file."""
    f = tmp_path / "another_valid.toml"
    f.write_text("name = 'test'\nenabled = true\n")
    return f


class TestValidToml:
    """Tests for valid TOML files."""

    def test_valid_file_returns_zero(self, valid_toml: Path) -> None:
        """Valid TOML file should return exit code 0."""
        result = subprocess.run(
            [*TOMLLINT_CMD, str(valid_toml)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_pyproject_toml_is_valid(self) -> None:
        """The project's own pyproject.toml should be valid."""
        result = subprocess.run(
            [*TOMLLINT_CMD, "pyproject.toml"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0


class TestInvalidToml:
    """Tests for invalid TOML files."""

    def test_invalid_file_returns_one(self, invalid_toml: Path) -> None:
        """Invalid TOML file should return exit code 1."""
        result = subprocess.run(
            [*TOMLLINT_CMD, str(invalid_toml)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1

    def test_error_format(self, invalid_toml: Path) -> None:
        """Error message should follow format: filename:line:col: error: message."""
        result = subprocess.run(
            [*TOMLLINT_CMD, str(invalid_toml)],
            capture_output=True,
            text=True,
        )
        # Error format: filename:line:col: error: message
        assert str(invalid_toml) in result.stderr
        assert ":1:" in result.stderr  # line 1
        assert ": error:" in result.stderr


class TestStdin:
    """Tests for stdin input."""

    def test_stdin_valid_toml(self) -> None:
        """Valid TOML from stdin should return exit code 0."""
        result = subprocess.run(
            [*TOMLLINT_CMD, "-"],
            input='key = "value"\n',
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_stdin_invalid_toml(self) -> None:
        """Invalid TOML from stdin should return exit code 1."""
        result = subprocess.run(
            [*TOMLLINT_CMD, "-"],
            input='key = "unclosed\n',
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1

    def test_stdin_error_shows_stdin_filename(self) -> None:
        """Error from stdin should show <stdin> as filename."""
        result = subprocess.run(
            [*TOMLLINT_CMD, "-"],
            input='key = "unclosed\n',
            capture_output=True,
            text=True,
        )
        assert "<stdin>:" in result.stderr


class TestMultipleFiles:
    """Tests for multiple file handling."""

    def test_multiple_valid_files(self, valid_toml: Path, another_valid_toml: Path) -> None:
        """Multiple valid files should return exit code 0."""
        result = subprocess.run(
            [*TOMLLINT_CMD, str(valid_toml), str(another_valid_toml)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_one_invalid_among_valid(
        self, valid_toml: Path, invalid_toml: Path, another_valid_toml: Path
    ) -> None:
        """If any file is invalid, return exit code 1."""
        result = subprocess.run(
            [*TOMLLINT_CMD, str(valid_toml), str(invalid_toml), str(another_valid_toml)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1


class TestErrorHandling:
    """Tests for error handling."""

    def test_nonexistent_file(self, tmp_path: Path) -> None:
        """Nonexistent file should produce a clean diagnostic, not a traceback."""
        nonexistent = tmp_path / "does_not_exist.toml"
        result = subprocess.run(
            [*TOMLLINT_CMD, str(nonexistent)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert f"{nonexistent}:0:0: error:" in result.stderr
        assert "Traceback" not in result.stderr

    def test_nonexistent_then_valid_continues(self, tmp_path: Path, valid_toml: Path) -> None:
        """A bad file should not abort the run; later files are still checked."""
        nonexistent = tmp_path / "does_not_exist.toml"
        result = subprocess.run(
            [*TOMLLINT_CMD, "--verbose", str(nonexistent), str(valid_toml)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert f"{nonexistent}:0:0: error:" in result.stderr
        assert f"{valid_toml}:1:1: info: linted successfully" in result.stderr


class TestVerbose:
    """Tests for the --verbose / -v flag."""

    def test_valid_file_verbose_long(self, valid_toml: Path) -> None:
        """Valid file with --verbose: exit 0, info diagnostic on stderr."""
        result = subprocess.run(
            [*TOMLLINT_CMD, "--verbose", str(valid_toml)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert f"{valid_toml}:1:1: info: linted successfully" in result.stderr

    def test_valid_file_verbose_short(self, valid_toml: Path) -> None:
        """Valid file with -v: same as --verbose."""
        result = subprocess.run(
            [*TOMLLINT_CMD, "-v", str(valid_toml)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert f"{valid_toml}:1:1: info: linted successfully" in result.stderr

    def test_invalid_file_verbose_no_success_line(self, invalid_toml: Path) -> None:
        """Invalid file with --verbose: error line, no success line."""
        result = subprocess.run(
            [*TOMLLINT_CMD, "--verbose", str(invalid_toml)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert ": error:" in result.stderr
        assert "info: linted successfully" not in result.stderr

    def test_multiple_valid_files_verbose(self, valid_toml: Path, another_valid_toml: Path) -> None:
        """Multiple valid files with --verbose: one success line each."""
        result = subprocess.run(
            [*TOMLLINT_CMD, "--verbose", str(valid_toml), str(another_valid_toml)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert f"{valid_toml}:1:1: info: linted successfully" in result.stderr
        assert f"{another_valid_toml}:1:1: info: linted successfully" in result.stderr

    def test_stdin_verbose(self) -> None:
        """Valid stdin with --verbose: <stdin> success line."""
        result = subprocess.run(
            [*TOMLLINT_CMD, "--verbose", "-"],
            input='key = "value"\n',
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "<stdin>:1:1: info: linted successfully" in result.stderr
