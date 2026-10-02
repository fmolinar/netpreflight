from netpreflight.assertions import evaluate_equals
from netpreflight.models import CheckDefinition, ValidationResult
from netpreflight.path import get_path


def run_equals_check(
    device: str,
    data: object,
    check: CheckDefinition,
) -> ValidationResult:
    actual = get_path(data, check.path)

    return evaluate_equals(
        device=device,
        check_name=check.name,
        actual=actual,
        expected=check.expected,
    )
