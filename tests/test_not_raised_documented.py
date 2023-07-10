from docraise.analyzer import Analyzer
from docraise.violation import ViolationCodes


# TODO: Check the exception type


def test_not_raised_documented(code_sample_not_raised_documented):
    # Arrange
    code_sample, expected_exc_names = code_sample_not_raised_documented
    analyzer = Analyzer()

    # Act
    violations = analyzer.validate(code_sample)

    # Assert
    assert len(violations) == len(expected_exc_names)
    assert all(violation.code == 'DR002' for violation in violations)
    assert all(violation.text == ViolationCodes.DR002.value.format(name=exc_name)
               for violation, exc_name
               in zip(violations, expected_exc_names)
               )
