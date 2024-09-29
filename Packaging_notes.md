# Packaging notes

## Test PyPi

```bash
rimraf .\dist\

python -m build

python -m twine upload --repository testpypi dist/* --verbose

```

## Installation

```bash
pip install -i https://test.pypi.org/simple/ graphedexcel
```
