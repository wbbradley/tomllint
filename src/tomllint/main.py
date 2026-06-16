"""tomllint - A simple TOML syntax checker.

Uses Python's built-in tomllib to validate TOML files.
Outputs errors in a standard format: filename:line:col: error: message
"""

import argparse
import re
import sys
import tomllib
from typing import BinaryIO, List, NamedTuple


def get_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for tomllint."""
    parser = argparse.ArgumentParser()
    parser.add_argument("toml_file", help='TOML filenames or "-" for stdin', nargs="+")
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="emit an info diagnostic for each file that lints successfully",
    )
    return parser


class Args(NamedTuple):
    filenames: List[str]
    from_stdin: bool
    verbose: bool


def get_args() -> Args:
    """Parse command-line arguments and return an Args tuple.

    Handles the special case of "-" to indicate reading from stdin.
    """
    parser = get_parser()
    args = parser.parse_args()
    from_stdin = args.toml_file == ["-"]
    return Args(
        filenames=["<stdin>"] if from_stdin else args.toml_file,
        from_stdin=from_stdin,
        verbose=args.verbose,
    )


def check_file(file: BinaryIO, filename: str, verbose: bool) -> int:
    """Validate a TOML file and print any errors to stderr.

    Returns 0 on success, 1 if the file contains invalid TOML. When verbose is
    true, a successful lint emits an info diagnostic to stderr.
    """
    try:
        tomllib.load(file)
    except tomllib.TOMLDecodeError as e:
        # tomllib doesn't expose structured error info, so we parse the message.
        m = re.match(r"(.*)\(at line (\d+), column (\d+)\)", str(e))
        if not m:
            print(e, file=sys.stderr)
        else:
            print(f"{filename}:{m[2]}:{m[3]}: error: {m[1].strip()}", file=sys.stderr)
        return 1
    if verbose:
        print(f"{filename}:1:1: info: linted successfully", file=sys.stderr)
    return 0


def main() -> None:
    """Entry point for tomllint. Exits with 0 if all files are valid, 1 otherwise."""
    args = get_args()
    error_code = 0
    if args.from_stdin:
        error_code |= check_file(file=sys.stdin.buffer, filename="<stdin>", verbose=args.verbose)
    else:
        for filename in args.filenames:
            try:
                with open(filename, "rb") as f:
                    error_code |= check_file(file=f, filename=filename, verbose=args.verbose)
            except OSError as e:
                print(f"{filename}:0:0: error: {e.strerror}", file=sys.stderr)
                error_code = 1
    sys.exit(error_code)


if __name__ == "__main__":
    main()
