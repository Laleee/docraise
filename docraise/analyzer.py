"""
This module contains the Analyzer class, a custom AST node visitor that
tracks exceptions in Python code. It checks for two types of violations:
1. Exceptions that are raised but not documented in the function's docstring.
2. Exceptions that are documented in the function's docstring but are not actually raised.

Example:
    To use this module, import it and create an instance of the Analyzer class.
    Then pass a Python AST to the Analyzer's visit method.

        from analyzer import Analyzer
        import ast

        analyzer = Analyzer()
        with open('file_to_analyze.py') as f:
            tree = ast.parse(f.read())
        violations = analyzer.check(tree)

    The method check returns a list of violations (instances of Violation class).
"""

import ast
from ast import NodeVisitor
from typing import Any, List, Optional

from docstring_parser import parse

from docraise.violation import Violation, ViolationCodes


class Analyzer(NodeVisitor):
    """
    A custom AST node visitor class that tracks exceptions in Python code.

    Attributes:
        violations: A list of detected violations.
        curr_func: The current function being visited.
        curr_filename: The current file being visited.
        exceptions: A list of exceptions detected in the current function.
    """

    def __init__(self):
        """Initialize the analyzer with empty violations, curr_func, and exceptions."""

        # If the violation is None that means that the user called just raise within the catch block
        # TODO: Ignore violations?
        self.violations: List[Violation] = []

        self.curr_func: Optional[ast.FunctionDef] = None
        self.curr_filename: Optional[str] = None

        # Exception names or None if exception is not named (e.g., just raise within an except block)
        self.exceptions: List[Optional[str]] = []

    def validate(
        self, tree: ast.AST, filename: str = "Unknown file"
    ) -> List[Violation]:
        self.curr_filename = filename
        self.violations = []

        self.visit(tree)

        self.curr_filename = None

        return self.violations

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        """
        Visit a function definition in the AST and checks for violations.

        This method is automatically called by NodeVisitor.generic_visit.

        Args:
            node (FunctionDef): The function definition node in the AST.
        """
        if self.curr_func is None:
            self.curr_func = node
        else:
            print(
                f"Error: Nested functions are not supported. Skipping '{self.curr_filename}:{node.lineno} {node.name}'"
            )
            return

        self.generic_visit(node)

        # TODO: Skip function if it doesn't have docstring?
        docstr = parse(ast.get_docstring(node))
        documented_exceptions = [e.type_name for e in docstr.raises]

        # raised but not documented
        for exception in self.exceptions:
            if exception not in documented_exceptions:
                assert exception is not None  # TODO: mypy error, handle better
                assert self.curr_filename is not None

                violation = Violation.from_code(
                    self.curr_filename, node.lineno, ViolationCodes.DR001, exception
                )
                self.violations.append(violation)

        # TODO: should be able to silence
        for exception in documented_exceptions:
            if exception not in self.exceptions:
                assert exception is not None  # TODO: mypy error, handle better
                assert self.curr_filename is not None

                violation = Violation.from_code(
                    self.curr_filename, node.lineno, ViolationCodes.DR002, exception
                )
                self.violations.append(violation)

        self.curr_func = None
        self.exceptions = []

    def visit_Raise(self, node: ast.Raise) -> Any:
        """
        Visit a raise statement in the AST and checks for violations.

        This method is automatically called by NodeVisitor.generic_visit.

        Args:
            node (Raise): The raise statement node in the AST.
        """
        if isinstance(node.exc, ast.Name):
            self.exceptions.append(node.exc.id)
        elif isinstance(node.exc, ast.Call):
            if isinstance(node.exc.func, ast.Name):
                self.exceptions.append(node.exc.func.id)
            elif isinstance(node.exc.func, ast.Attribute):
                self.exceptions.append(node.exc.func.attr)
            else:
                raise AssertionError("Case not covered")
        elif isinstance(node.exc, ast.Attribute):
            self.exceptions.append(node.exc.attr)
        else:
            self.exceptions.append(None)

        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> Any:
        """
        Visit an exception handler in the AST and checks for violations.

        This method is automatically called by NodeVisitor.generic_visit.

        Args:
            node (ExceptHandler): The exception handler node in the AST.

        Raises:
            (specific exceptions this method can raise)
        """

        self.generic_visit(node)

        if self.exceptions:
            latest_exception = self.exceptions.pop()

            if latest_exception is None:  # only used raise
                if isinstance(node.type, ast.Name):
                    # This exception will be raised
                    self.exceptions.append(node.type.id)
                elif isinstance(node.type, ast.Tuple):
                    # These exceptions will be raised
                    exceptions: List[ast.Name] = [
                        n for n in node.type.elts if isinstance(n, ast.Name)
                    ]

                    assert len(exceptions) == len(
                        node.type.elts
                    ), "Case not covered"  # All are of type ast.Name

                    self.exceptions.extend(e.id for e in exceptions)
                elif node.type is None:
                    # Only raise
                    """
                    try:
                        pass
                    except:
                        raise
                    """
                    # In this case the exception documentation will be ignored since it's missing a name
                    pass
                else:
                    raise AssertionError("Case not covered")
            elif latest_exception == node.name:  # e.g., raise e
                # Switch name with the actual exception name
                if isinstance(node.type, ast.Name):  # e.g., except ValueError as e
                    self.exceptions.append(node.type.id)
                elif isinstance(
                    node.type, ast.Tuple
                ):  # e.g., except (ValueError, AttributeError) as e
                    _exceptions: List[ast.Name] = [  # _ because of mypy no-redef
                        n for n in node.type.elts if isinstance(n, ast.Name)
                    ]

                    assert len(_exceptions) == len(
                        node.type.elts
                    ), "Case not covered"  # All must be names

                    self.exceptions.extend(e.id for e in _exceptions)
                else:
                    raise AssertionError("Case not covered")
            else:  # raise ValueError, raise ValueError()
                self.exceptions.append(latest_exception)
