# Changelog

## [0.3.5] - 2026-07-31

### Changed
- Corrected the project license from MIT to MIT No Attribution (MIT-0).

## [0.3.4] - 2026-07-31

### Changed
- Relicensed the project from CC0 1.0 Universal to the MIT License, with
  copyright © 2026 Will Bradley.

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
