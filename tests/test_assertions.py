from netpreflight.assertions import evaluate_equals


def test_equals_passes_when_values_match() -> None:
    result = evaluate_equals(
        device="router1",
        check_name="Uplink is operational",
        actual="up",
        expected="up",
    )

    assert result.passed is True
    assert result.status == "PASS"
    assert result.device == "router1"
    assert result.check_name == "Uplink is operational"
    assert result.actual == "up"
    assert result.expected == "up"
    assert result.message is None


def test_equals_fails_when_values_differ() -> None:
    result = evaluate_equals(
        device="router1",
        check_name="Uplink is operational",
        actual=1500,
        expected=2000,
    )

    assert result.passed is False
    assert result.status == "FAIL"
    assert result.device == "router1"
    assert result.message == "Expected 2000, but received 1500"
    assert result.actual == 1500
    assert result.expected == 2000


def test_equals_handles_none() -> None:
    result = evaluate_equals(
        device="router1",
        check_name="Uplink is operational",
        actual=None,
        expected="0.0.0.0/0",
    )

    assert result.passed is False
    assert result.message == "Expected 0.0.0.0/0, but received None"


def test_equals_compares_structured_values() -> None:
    result = evaluate_equals(
        device="router1",
        check_name="OSPF neighbor state",
        actual={"status": "FULL"},
        expected={"status": "FULL"},
    )

    assert result.passed is True
