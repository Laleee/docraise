from docraise.analyzer import Analyzer


# TODO: Check the exception type


def test_raised_not_documented(code_sample_raised_not_documented):
    # Arrange
    analyzer = Analyzer()

    # Act
    analyzer.validate(code_sample_raised_not_documented)

    # Assert
    assert len(analyzer.violations) == 1
    assert analyzer.violations[0].code == 'DR001'
