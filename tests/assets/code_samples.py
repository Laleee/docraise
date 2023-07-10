import textwrap

# TODO: Note somewhere: Cannot detect ZeroDivisionError from return a / b (out of the project scope)
# TODO: Raised but documented wrong exception - subtype of raised not documented?
# TODO: README note - Raises vs Raises:

raised_not_documented = {
    # sample name: (sample_string, expected_exceptions)
    "raise an instance of value error": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        if b == 0:
            raise ValueError()
        return a / b
    """), ["ValueError"]),
    "raise value error class": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        if b == 0:
            raise ValueError
        return a / b
    """), ["ValueError"]),
    "raise class attribute exc": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        if b == 0:
            raise exc.ValueError
        return a / b
    """), ["ValueError"]),
    "raise class attribute instance": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        if b == 0:
            raise exc.ValueError()
        return a / b
    """), ["ValueError"]),
    "reraise": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except ZeroDivisionError:
            raise
    """), ["ZeroDivisionError"]),
    "reraise named": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except ZeroDivisionError as e:
            raise e
    """), ["ZeroDivisionError"]),
    "exception instance chaining": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except ZeroDivisionError as e:
            raise ValueError() from e
    """), ['ValueError']),
    "exception class chaining": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except ZeroDivisionError as e:
            raise ValueError from e
    """), ["ValueError"]),
    "multi-exception catch raise from": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except (SomeError, ZeroDivisionError) as e:
            raise ValueError from e
    """), ["ValueError"]),
    "multi-exception catch just raise": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except (SomeError, ZeroDivisionError):
            raise
    """), ["SomeError", "ZeroDivisionError"]),
    "multi-exception catch named": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except (SomeError, ZeroDivisionError) as e:
            raise e
    """), ["SomeError", "ZeroDivisionError"]),
    # Special test case: Cannot determine the name -> Cannot require docstring raise
    "empty except": (textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except:
            raise
    """), []),
}

not_raised_documented = {
    "basic": (textwrap.dedent("""
    def add(a, b):
        '''
        Add a and b.

        Raises:
            TypeError: If a or b is not an integer.
        '''
        return a + b  # Does not actually raise TypeError.
    """), ["TypeError"]),
    "multiple": (textwrap.dedent("""
    def add(a, b):
        '''
        Add a and b.

        Raises:
            TypeError: If a or b is not an integer.
            SomeError: If some error occurs
        '''
        return a + b  # Does not actually raise TypeError.
    """), ["TypeError", "SomeError"]),
    "partially ok": (textwrap.dedent("""
    def add(a, b):
        '''
        Add a and b.

        Raises:
            TypeError: If a or b is not an integer.
            DocumentedError: If some error occurs
        '''
        if a < 0:
            raise DocumentedError
        return a + b  # Does not actually raise TypeError.
    """), ["TypeError"]),
}

not_raised_not_documented = {
    "basic": textwrap.dedent("""
    def add(a, b):
        '''Add a and b.'''
        return a + b  # Does not actually raise TypeError.
    """),
    "ignored except block": textwrap.dedent("""
    def divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            pass
    """),
    "ignored raw except block": textwrap.dedent("""
    def divide(a, b):
        try:
            return a / b
        except:
            pass
    """),
}
# TODO: finally block

raised_documented = {
    "raise an instance of value error": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            ValueError: if b is zero
        '''
        if b == 0:
            raise ValueError()  # Raise an instance of value error
        return a / b
    """),
    "raise value error class": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            ValueError: if b is zero
        '''
        if b == 0:
            raise ValueError  # Raise value error class
        return a / b
    """),
    # This or require exc.ValueError in docstring
    "raise class attribute class": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            ValueError: if b is zero
        '''
        if b == 0:
            raise exc.ValueError
        return a / b
    """),
    "raise class attribute instance": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            ValueError: if b is zero
        '''
        if b == 0:
            raise exc.ValueError()
        return a / b
    """),
    "reraise": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            ZeroDivisionError: if b is zero
        '''
        try:
            return a / b
        except ZeroDivisionError:
            raise
    """),
    "reraise named": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            ZeroDivisionError: if b is zero
        '''
        try:
            return a / b
        except ZeroDivisionError as e:
            raise e
    """),
    "exception instance chaining": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            ValueError: if b is zero
        '''
        try:
            return a / b
        except ZeroDivisionError as e:
            raise ValueError() from e
    """),
    "exception class chaining": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            ValueError: if b is zero
        '''
        try:
            return a / b
        except ZeroDivisionError as e:
            raise ValueError from e
    """),
    "multi-exception catch just raise": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            SomeError: on error
            ZeroDivisionError: again on error
        '''
        try:
            return a / b
        except (SomeError, ZeroDivisionError):
            raise
    """),
    "multi-exception catch named": textwrap.dedent("""
    def divide(a, b):
        '''
        Divide a by b.

        Raises:
            SomeError: on error
            ZeroDivisionError: again on error
        '''
        try:
            return a / b
        except (SomeError, ZeroDivisionError) as e:
            raise e
    """)
}
