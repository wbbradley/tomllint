"""Tests for the tomllint manual page."""

import re
import subprocess
import sys
from pathlib import Path

MANPAGE = Path(__file__).parents[1] / "man" / "tomllint.1"


def test_manpage_has_required_sections() -> None:
    """The manual page should contain all user-facing sections."""
    source = MANPAGE.read_text()
    for section in (
        "NAME",
        "SYNOPSIS",
        "DESCRIPTION",
        "OPTIONS",
        "EXIT STATUS",
        "DIAGNOSTICS",
        "EXAMPLES",
        "SEE ALSO",
    ):
        assert f".SH {section}\n" in source


def test_manpage_documents_every_option() -> None:
    """Every option shown by the CLI should appear in the manual page."""
    source = MANPAGE.read_text()
    result = subprocess.run(
        [sys.executable, "-m", "tomllint.main", "--help"],
        capture_output=True,
        check=True,
        text=True,
    )
    options_help = result.stdout.split("options:\n", maxsplit=1)[1]
    option_strings = set(re.findall(r"(?<!\w)--?[a-z][a-z-]*", options_help))

    assert option_strings
    for option in option_strings:
        assert option.replace("-", r"\-") in source
