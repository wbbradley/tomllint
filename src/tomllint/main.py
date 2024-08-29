import argparse
import re
import sys
import tomllib
from typing import BinaryIO, NamedTuple


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help='filename or "-" for stdin')
    return parser


class State(NamedTuple):
    file: BinaryIO
    filename: str
    from_stdin: bool


def parse_args_into_state() -> State:
    parser = get_parser()
    args = parser.parse_args()
    from_stdin = args.input == "-"
    return State(
        filename="<stdin" if from_stdin else args.input,
        file=sys.stdin.buffer if from_stdin else open(args.input, "rb"),
        from_stdin=from_stdin,
    )


def main() -> None:
    state = parse_args_into_state()

    try:
        tomllib.load(state.file)
    except tomllib.TOMLDecodeError as e:
        # This is dumb. I should find a better TOML library, but this one is builtin.
        m = re.match(r"(.*)\(at line (\d+), column (\d+)\)", str(e))
        if not m:
            print(e, file=sys.stderr)
        else:
            print(f"{state.filename}:{m[2]}:{m[3]}: error: {m[1].strip()}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
