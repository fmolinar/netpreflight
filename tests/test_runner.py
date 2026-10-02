import pytest

from netpreflight.models import CheckDefinition
from netpreflight.path import PathNotFoundError
from netpreflight.runner import run_equals_check


def test_run_equals_check_passes() -> None:
    data = {
        "interfaces": {
            "GigabitEthernet1": {
                "oper_status": "up",
            }
        }
    }
    check = CheckDefinition(
        name="Uplink is operational",
        path=("interfaces", "GigabitEthernet1", "oper_status"),
        expected="up",
    )

    result = run_equals_check(
        device="router1",
        data=data,
        check=check,
    )

    assert result.passed is True
    assert result.actual == "up"
    assert result.expected == "up"
    assert result.device == "router1"
    assert result.check_name == "Uplink is operational"


def test_run_equals_check_fails() -> None:
    data = {
        "interfaces": {
            "GigabitEthernet1": {
                "oper_status": "down",
            }
        }
    }
    check = CheckDefinition(
        name="Uplink is operational",
        path=("interfaces", "GigabitEthernet1", "oper_status"),
        expected="up",
    )

    result = run_equals_check(
        device="router1",
        data=data,
        check=check,
    )

    assert result.passed is False
    assert result.actual == "down"
    assert result.message == "Expected up, but received down"


def test_run_equals_check_propagates_missing_path() -> None:
    data = {"interfaces": {}}
    check = CheckDefinition(
        name="Uplink is operational",
        path=("interfaces", "GigabitEthernet1", "oper_status"),
        expected="up",
    )

    with pytest.raises(PathNotFoundError):
        run_equals_check(
            device="router1",
            data=data,
            check=check,
        )
