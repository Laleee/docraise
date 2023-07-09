import textwrap

# TODO: Note somewhere: Cannot detect ZeroDivisionError from return a / b (out of the project scope)
# TODO: Raised but documented wrong exception - subtype of raised not documented?
# TODO: README note - Raises vs Raises:

raised_not_documented = {
    "raise an instance of value error": textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        if b == 0:
            raise ValueError()
        return a / b
    """),
    "raise value error class": textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        if b == 0:
            raise ValueError
        return a / b
    """),
    "reraise": textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except ZeroDivisionError:
            raise
    """),
    "reraise named": textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except ZeroDivisionError as e:
            raise e
    """),
    "exception instance chaining": textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except ZeroDivisionError as e:
            raise ValueError() from e
    """),
    "exception class chaining": textwrap.dedent("""
    def divide(a, b):
        '''Divide a by b.'''
        try:
            return a / b
        except ZeroDivisionError as e:
            raise ValueError from e
    """)
}

not_raised_documented = {
    "basic": textwrap.dedent("""
    def add(a, b):
        '''
        Add a and b.

        Raises:
            TypeError: If a or b is not an integer.
        '''
        return a + b  # Does not actually raise TypeError.
    """)
}

not_raised_not_documented = {
    "basic": textwrap.dedent("""
    def add(a, b):
        '''Add a and b.'''
        return a + b  # Does not actually raise TypeError.
    """)
}

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
    """)
}
