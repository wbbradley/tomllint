# Dev docs

## Development steps

```sh
./setup-env -f
```

## Publish steps

```sh
rm -rf dist/
.venv/bin/python -m build
.venv/bin/twine upload dist/*
```
