import argparse
import re
import sys
import tomllib
from typing import List, BinaryIO, NamedTuple


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("toml_file", help='TOML filenames or "-" for stdin', nargs="+")
    return parser


class Args(NamedTuple):
    filenames: List[str]
    from_stdin: bool


def get_args() -> Args:
    parser = get_parser()
    args = parser.parse_args()
    from_stdin = args.toml_file == ["-"]
    return Args(
        filenames=["<stdin>"] if from_stdin else args.toml_file,
        from_stdin=from_stdin,
    )


def check_file(file: BinaryIO, filename: str) -> int:
    try:
        tomllib.load(file)
    except tomllib.TOMLDecodeError as e:
        # This is dumb. I should find a better TOML library, but this one is builtin.
        m = re.match(r"(.*)\(at line (\d+), column (\d+)\)", str(e))
        if not m:
            print(e, file=sys.stderr)
        else:
            print(f"{filename}:{m[2]}:{m[3]}: error: {m[1].strip()}", file=sys.stderr)
        return 1


def main() -> None:
    args = get_args()
    error_code = 0
    if args.from_stdin:
        error_code |= check_file(file=sys.stdin.buffer, filename="<stdin>")
    else:
        for filename in args.filenames:
            error_code |= check_file(file=open(filename, "rb"), filename=filename)
    sys.exit(error_code)


if __name__ == "__main__":
    main()
