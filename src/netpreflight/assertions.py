from netpreflight.models import ValidationResult


def evaluate_equals(
    device: str, check_name: str, actual: object, expected: object
) -> ValidationResult:
    """
    Evaluates whether the actual value equals the expected value.

    Args:
        device (str): The name of the device being checked.
        check_name (str): The name of the check being performed.
        actual (object): The actual value obtained from the device.
        expected (object): The expected value to compare against.

    Returns:
        ValidationResult: An object containing the result of the evaluation.
    """
    passed = actual == expected
    message = None if passed else f"Expected {expected}, but received {actual}"

    return ValidationResult(
        device=device,
        check_name=check_name,
        actual=actual,
        expected=expected,
        passed=passed,
        message=message,
    )
