# Changelog

## [0.3.3] - 2026-06-16

### Added
- `--verbose` / `-v` flag: emits a `filename:1:1: info: linted successfully`
  diagnostic on stderr for each file that lints cleanly (silent on success by default).

### Fixed
- Unopenable files (missing, unreadable) now produce a clean
  `filename:0:0: error: <reason>` diagnostic instead of an uncaught Python traceback,
  and the run continues to the remaining files instead of aborting.

## [0.3.2]

### Added
- pre-commit integration instructions in the README.
