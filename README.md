# Docraise

Docraise is a Python project that checks whether the docstrings in your Python code contain valid "Raises" sections.
It ensures that every exception your code raises is documented in the docstrings, and vice versa - that every exception documented in the docstrings is actually raised by the code.

## Installation

Install the project dependencies:

```bash
pip install -r requirements-dev.txt
```

## pre-commit setup

Docraise uses [pre-commit](https://pre-commit.com/) to manage git hooks. This helps to ensure that code style, tests, and other checks are run before each commit.

We use the following pre-commit plugins:

- [black](https://github.com/psf/black): Ensures our Python code adheres to the Black code style.
- [flake8](https://flake8.pycqa.org/en/latest/): Lints our Python code to catch potential bugs.
- [isort](https://pycqa.github.io/isort/): Sorts our Python imports.
- [mypy](http://mypy-lang.org/): Checks our Python code for type errors.
- [pydocstyle](http://www.pydocstyle.org/en/stable/): Checks our Python docstrings to ensure they adhere to the docstring conventions.
- [conventional commit](https://www.conventionalcommits.org/): Ensures all commit messages adhere to the Conventional Commits style.

In the project directory, install the pre-commit hooks:
```bash
pre-commit install
pre-commit install --hook-type commit-msg
```


## Usage

TODO

## Testing

TODO

```bash
pytest tests/
```
