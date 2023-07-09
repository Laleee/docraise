import ast
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

import click

import docraise
from docraise.analyzer import Analyzer

# def get_python_files(path: str) -> List[str]:
#     """Walk through the given directory and return python files.
#
#     Args:
#         path (str): The path to the directory to analyze.
#
#     Returns:
#         List[str]: A list of paths to Python files in the directory.
#     """
#     python_files = []
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             if file.endswith(".py"):
#                 python_files.append(os.path.join(root, file))
#     return python_files


def get_function_defs(tree: ast.AST):
    """Extract all function definitions from an AST.

    Args:
        tree (ast.AST): The abstract syntax tree to extract from.

    Returns:
        List[ast.FunctionDef]: A list of all function definitions in the tree.
    """
    return [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_python_files(path: Path) -> List[Path]:
    """Walk through the given directory and return python files.

    Args:
        path (Path): The path to the directory to analyze.

    Returns:
        List[Path]: A list of paths to Python files in the directory.
    """
    return list(path.rglob("*.py"))


def process_paths(paths: Iterable[str]) -> List[Path]:
    """Process a list of paths, returning a list of all Python files in those paths.

    Args:
        paths (Iterable[str]): A list of paths to files or directories.

    Returns:
        List[Path]: A list of paths to Python files in the provided paths.
    """
    python_files = []
    for pth in paths:
        path: Path = Path(pth).resolve()
        if path.is_file() and path.suffix == ".py":
            python_files.append(path)
        elif path.is_dir():
            python_files.extend(get_python_files(path))
    return python_files


@click.command()
@click.argument("paths", nargs=-1)
@click.version_option(docraise.__version__)
def main(paths: Tuple[str]) -> None:
    """Command line interface for the program.

    Args:
        paths (Tuple[str]): A tuple of paths to files or directories.
    """
    # TODO: Option to exclude files
    python_files = process_paths(paths)

    python_trees = []
    for filename in python_files:
        with open(filename, "r") as source:
            python_trees.append(ast.parse(source.read()))

    results = []
    for filename, tree in zip(python_files, python_trees):
        # TODO: Cover failed Python parsing
        analyzer = Analyzer()

        violations = analyzer.validate(tree, str(filename))

        results.extend(violations)

    for violation in results:
        print(violation)

    if results:
        sys.exit(1)  # TODO: ctx.exit

    sys.exit(0)


if __name__ == "__main__":
    main()
