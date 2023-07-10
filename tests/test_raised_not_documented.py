from docraise.analyzer import Analyzer
from docraise.violation import ViolationCodes


# TODO: Check the exception type


def test_raised_not_documented(code_sample_raised_not_documented):
    # Arrange
    code_sample, expected_exc_names = code_sample_raised_not_documented
    analyzer = Analyzer()

    # Act
    violations = analyzer.validate(code_sample)

    # Assert
    assert len(violations) == len(expected_exc_names)
    assert all(violation.code == 'DR001' for violation in violations)
    assert all(violation.text == ViolationCodes.DR001.value.format(name=exc_name)
               for violation, exc_name
               in zip(violations, expected_exc_names)
               )
