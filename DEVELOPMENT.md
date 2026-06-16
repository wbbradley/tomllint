# Development Guide

## Setup

1.  **Create and activate the development environment:**

```bash
./setup-env
source .venv/bin/activate
```

To recreate the environment from scratch:

```bash
./setup-env -f
source .venv/bin/activate
```

2. **Install the package in editable mode:**

```bash
+pip install -e .
```
This step is crucial if you want to manually test the tool. It makes your local tomllint source code available to your shell, allowing you to run commands like `tomllint` or `python -m tomllint.main`.

## Running Tests

Run all tests:

```bash
pytest tests/ -v
```

Run a specific test class:

```bash
pytest tests/test_main.py::TestStdin -v
```

Run a specific test:

```bash
pytest tests/test_main.py::TestValidToml::test_valid_file_returns_zero -v
```

## Linting and Formatting

Check for linting issues:

```bash
ruff check src/ tests/
```

Check formatting:

```bash
ruff format --check src/ tests/
```

Auto-fix formatting:

```bash
ruff format src/ tests/
```

## Type Checking

Run mypy:

```bash
mypy src/tomllint/main.py
```

## Publishing

```bash
rm -rf dist/
.venv/bin/python -m build
.venv/bin/twine upload dist/*
```

## Manual Testing

Test with a valid TOML file:

```bash
python -m tomllint.main pyproject.toml
```

Test with stdin:

```bash
cat pyproject.toml | python -m tomllint.main -
```

Test with multiple files:

```bash
python -m tomllint.main pyproject.toml pyproject.toml
```

Test error output format with invalid TOML:

```bash
echo 'key = "unclosed' | python -m tomllint.main -
# Output: <stdin>:1:16: error: Illegal character '\n'
```

# Contributors

`tomllint` was made possible by the following contributors:

- @wbbradley
- @Taffer

If you'd like to contribute to `tomllint`, please feel free to open an issue or submit a pull request!
