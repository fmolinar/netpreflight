import argparse
from collections.abc import Sequence

from netpreflight import __version__


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="netpreflight",
        description="Validate network state before and after changes.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.parse_args(argv)
    parser.print_help()

    return 0
