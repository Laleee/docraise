from docraise.analyzer import Analyzer


# TODO: Check the exception type


def test_not_raised_documented(code_sample_not_raised_documented):
    # Arrange
    analyzer = Analyzer()

    # Act
    violations = analyzer.validate(code_sample_not_raised_documented)

    # Assert
    assert len(violations) == 1
    assert analyzer.violations[0].code == 'DR002'
