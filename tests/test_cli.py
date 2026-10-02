import pytest

from netpreflight.cli import main


def test_version_option(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as raised:
        main(["--version"])

    output = capsys.readouterr().out

    assert raised.value.code == 0
    assert output == "netpreflight 0.1.0\n"


def test_no_arguments_displays_help(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main([])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "usage: netpreflight" in output
