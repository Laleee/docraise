"""
This module defines the ViolationCodes enum and the Violation dataclass.

ViolationCodes is an enumeration of violation codes and their descriptions.
The codes correspond to two types of violations:
1. Exceptions that are raised but not documented in the function's docstring (DR001).
2. Exceptions that are documented in the function's docstring but are not actually raised (DR002).

Violation is a dataclass that encapsulates details about a detected violation,
including the line number where the violation was detected, the violation code, and a description of the violation.

Example:
    To use this module, import it and create instances of the Violation class using the from_code class method.

        from violation import Violation, ViolationCodes

        violation = Violation.from_code(10, ViolationCodes.DR001, 'MyException')
"""

import enum
from dataclasses import dataclass


class ViolationCodes(enum.Enum):
    """Enumeration of violation codes and their descriptions."""

    DR001 = 'Exception "{name}" raised but not documented'
    DR002 = 'Exception "{name}" documented but never raised'


@dataclass
class Violation:
    """
    Data class that encapsulates details about a detected violation.

    Attributes:
        lineno: The line number where the violation was detected.
        code: The violation code.
        text: The description of the violation.
    """

    filename: str
    lineno: int
    code: str
    text: str

    @classmethod
    def from_code(
        cls, filename: str, lineno: int, code: ViolationCodes, exc_name: str
    ) -> "Violation":
        """
        Factory method to create a Violation instance from a violation code.

        Args:
            filename (str): Name of the file where the violation was detected.
            lineno (int): The line number where the violation was detected.
            code (ViolationCodes): The violation code.
            exc_name (str): The name of the exception associated with the violation.

        Returns:
            Violation: A new Violation instance.
        """
        return cls(
            filename=filename,
            lineno=lineno,
            code=code.name,
            text=code.value.format(name=exc_name),
        )

    def __str__(self):
        return f"{self.filename}:{self.lineno}: \033[31m{self.code}\033[0m {self.text}"
