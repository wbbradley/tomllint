# tomllint

A TOML Linter. Checks for basic syntactic errors in any TOML file.

## Installation

```bash
$ pip install tomllint
```

## Usage

Usage is self explanatory, simply name the file to lint, or use `-` to indicate that it should read
from `stdin`.

```
usage: tomllint [-h] input

positional arguments:
  input       filename or "-" for stdin

options:
  -h, --help  show this help message and exit
```
