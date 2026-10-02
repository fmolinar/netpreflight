import pytest

from netpreflight.path import PathNotFoundError, get_path


def test_get_path_returns_nested_values() -> None:
    data = {
        "interfaces": {
            "GigabitEthernet1": {
                "oper_status": "up",
            }
        }
    }

    actual = get_path(
        data,
        ("interfaces", "GigabitEthernet1", "oper_status"),
    )

    assert actual == "up"


def test_get_path_supports_list_indexing() -> None:
    data = {
        "neighbors": [
            {"address": "192.0.2.1", "state": "FULL"},
            {"address": "192.0.2.2", "state": "FULL"},
        ]
    }

    actual = get_path(
        data,
        ("neighbors", 1, "state"),
    )

    assert actual == "FULL"


def test_get_path_preserve_keys_containing_periods() -> None:
    data = {
        "routes": {
            "0.0.0.0/0": {
                "next_hop": "192.0.2.1",
            }
        }
    }

    actual = get_path(
        data,
        ("routes", "0.0.0.0/0", "next_hop"),
    )

    assert actual == "192.0.2.1"


def test_get_path_raises_error_for_missing_key() -> None:
    data = {"interfaces": {}}

    with pytest.raises(
        PathNotFoundError,
        match="GigabitEthernet1",
    ):
        get_path(
            data,
            ("interfaces", "GigabitEthernet1", "oper_status"),
        )


def test_get_path_raises_error_for_invalid_list_index() -> None:
    data = {"neighbors": [{"state": "FULL"}]}

    with pytest.raises(PathNotFoundError, match="5"):
        get_path(data, ("neighbors", 5, "state"))


def test_get_path_rejects_negative_list_index() -> None:
    data = {"neighbors": [{"state": "FULL"}]}

    with pytest.raises(PathNotFoundError, match="-1"):
        get_path(data, ("neighbors", -1, "state"))
