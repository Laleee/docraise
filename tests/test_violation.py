from docraise.violation import Violation, ViolationCodes


def test_from_code():
    # Arrange
    lineno = 10
    code = ViolationCodes.DR001
    exc_name = 'MyException'

    # Act
    violation = Violation.from_code(__name__, lineno, code, exc_name)

    # Assert
    assert violation.filename == __name__
    assert violation.lineno == lineno
    assert violation.code == code.name
    assert violation.text == ViolationCodes.DR001.value.format(name='MyException')
