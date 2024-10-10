# Packaging notes

Notes on packaging and distributing the package.

## Test PyPi

```bash
rimraf .\dist\; python -m build; python -m twine upload --repository pypi dist/* --verbose

python -m build

python -m twine upload --repository testpypi dist/\* --verbose

```

## Installation

```bash
pip install -i https://test.pypi.org/simple/ graphedexcel
```

## installation from local dist

```bash
pip install 'C:\projects\dalager\1 Projects\graphedexcel\dist\graphedexcel-0.0.0-py3-none-any.whl' --force-reinstall

```

## Running locally

```bash
python -m build; pip install -e .
```
