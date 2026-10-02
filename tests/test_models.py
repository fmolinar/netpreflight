from dataclasses import FrozenInstanceError

import pytest

from netpreflight.models import ValidationResult


def test_passing_validation_result() -> None:
    result = ValidationResult(
        device="router1",
        check_name="Uplink is operational",
        passed=True,
        actual="up",
        expected="up",
    )

    assert result.device == "router1"
    assert result.check_name == "Uplink is operational"
    assert result.passed is True
    assert result.actual == "up"
    assert result.expected == "up"
    assert result.message is None
    assert result.status == "PASS"


def test_failing_validation_result() -> None:
    result = ValidationResult(
        device="router1",
        check_name="Default route exists",
        passed=False,
        actual=None,
        expected="0.0.0.0/0",
        message="Default route is missing",
    )

    assert result.passed is False
    assert result.status == "FAIL"
    assert result.message == "Default route is missing"


def test_validation_result_immutable() -> None:
    result = ValidationResult(
        device="router1",
        check_name="Uplink is operational",
        passed=True,
        actual="up",
        expected="up",
    )

    with pytest.raises(FrozenInstanceError):
        result.passed = False
