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
        analyzer.visit(tree)

    The violations are stored in the analyzer's 'violations' attribute as instances of the Violation class.
"""

import ast
from _ast import Call, ExceptHandler, FunctionDef, Name, Raise
from ast import NodeVisitor
from typing import Any, List, Optional, cast

from docstring_parser import parse

from docraise.violation import Violation, ViolationCodes


class Analyzer(NodeVisitor):
    """
    A custom AST node visitor class that tracks exceptions in Python code.

    Attributes:
        violations: A list of detected violations.
        curr_func: The current function being visited.
        exceptions: A list of exceptions detected in the current function.
    """

    def __init__(self):
        """Initialize the analyzer with empty violations, curr_func, and exceptions."""

        # If the violation is None that means that the user called just raise within the catch block
        self.violations: List[Optional[Violation]] = []

        self.curr_func: Optional[FunctionDef] = None

        # Exception names or None if exception is not named (e.g., just raise within an except block)
        self.exceptions: List[Optional[str]] = []

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        """
        Visit a function definition in the AST and checks for violations.

        This method is automatically called by NodeVisitor.generic_visit.

        Args:
            node (FunctionDef): The function definition node in the AST.
        """
        if self.curr_func is None:
            self.curr_func = node
        else:
            print("PRENK")

        self.generic_visit(node)

        docstr = parse(ast.get_docstring(node))
        documented_exceptions = [e.type_name for e in docstr.raises]

        # raised but not documented
        for exception in self.exceptions:
            if exception not in documented_exceptions:
                assert exception is not None  # TODO: mypy error, handle better

                violation = Violation.from_code(
                    node.lineno, ViolationCodes.DR001, exception
                )
                self.violations.append(violation)

        # TODO: should be able to silence
        for exception in documented_exceptions:
            if exception not in self.exceptions:
                assert exception is not None  # TODO: mypy error, handle better

                violation = Violation.from_code(
                    node.lineno, ViolationCodes.DR002, exception
                )
                self.violations.append(violation)

        self.curr_func = None
        self.exceptions = []

    def visit_Raise(self, node: Raise) -> Any:
        """
        Visit a raise statement in the AST and checks for violations.

        This method is automatically called by NodeVisitor.generic_visit.

        Args:
            node (Raise): The raise statement node in the AST.
        """
        if isinstance(node.exc, Name):
            self.exceptions.append(node.exc.id)
        elif isinstance(node.exc, Call):
            name_node = cast(Name, node.exc.func)  # Required for mypy error
            self.exceptions.append(name_node.id)
        else:
            self.exceptions.append(None)

        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ExceptHandler) -> Any:
        """
        Visit an exception handler in the AST and checks for violations.

        This method is automatically called by NodeVisitor.generic_visit.

        Args:
            node (ExceptHandler): The exception handler node in the AST.

        Raises:
            (specific exceptions this method can raise)
        """

        self.generic_visit(node)

        node_type = cast(Name, node.type)  # Required for mypy

        latest_exception = self.exceptions.pop()
        if latest_exception is None:  # only used raise
            # This exception will be raised
            self.exceptions.append(node_type.id)
        elif latest_exception == node.name:  # e.g., raise e
            # Switch name with the actual exception name
            self.exceptions.append(node_type.id)
        else:  # raise ValueError, raise ValueError()
            self.exceptions.append(latest_exception)