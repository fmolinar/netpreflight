from netpreflight.models import ValidationReport, ValidationResult
from netpreflight.reports.console import format_console_report


def test_format_console_report() -> None:
    report = ValidationReport(
        results=(
            ValidationResult(
                device="router1",
                check_name="Interface state",
                passed=True,
                actual="up",
                expected="up",
            ),
            ValidationResult(
                device="router1",
                check_name="Interface MTU",
                passed=False,
                actual=1500,
                expected=9000,
                message="Expected 9000, but received 1500",
            ),
        )
    )
    output = format_console_report(report)

    assert output == (
        "[PASS] router1 - Interface state\n"
        "[FAIL] router1 - Interface MTU: "
        "Expected 9000, but received 1500\n"
        "\n"
        "Summary: 1 passed, 1 failed"
    )


def test_format_empty_console_report() -> None:
    report = ValidationReport(results=())

    output = format_console_report(report)

    assert output == "Summary: 0 passed, 0 failed"
