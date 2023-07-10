import ast

import pytest

from tests.assets.code_samples import raised_documented, raised_not_documented, \
    not_raised_not_documented, not_raised_documented


@pytest.fixture(params=raised_not_documented.values(), ids=raised_not_documented.keys())
def code_sample_raised_not_documented(request):
    """Fixture that provides code samples as ASTs."""
    return ast.parse(request.param[0]), request.param[1]


@pytest.fixture(params=raised_documented.values(), ids=raised_documented.keys())
def code_sample_raised_documented(request):
    """Fixture that provides code samples as ASTs."""
    return ast.parse(request.param)


@pytest.fixture(params=not_raised_not_documented.values(), ids=not_raised_not_documented.keys())
def code_sample_not_raised_not_documented(request):
    """Fixture that provides code samples as ASTs."""
    return ast.parse(request.param)


@pytest.fixture(params=not_raised_documented.values(), ids=not_raised_documented.keys())
def code_sample_not_raised_documented(request):
    """Fixture that provides code samples as ASTs."""
    return ast.parse(request.param[0]), request.param[1]
