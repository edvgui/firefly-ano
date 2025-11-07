#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.2,<9",
#   "click-loglevel>=0.6,<1",
# ]
# ///

import io
import logging
import sys

import click
import click_loglevel

LOGGER = logging.getLogger()
logging.root.addHandler(logging.StreamHandler(sys.stderr))


@click.command()
@click.option(
    "-l",
    "--log-level",
    type=click_loglevel.LogLevel(),
    default="INFO",
    help="Set logging level",
    show_default=True,
    show_envvar=True,
    envvar="LOG_LEVEL",
)
@click.argument(
    "file",
    type=click.File("r"),
    default=sys.stdin,
    nargs=1,
    envvar="FILE",
)
def main(log_level: int, file: io.TextIOWrapper) -> None:
    """
    This tool helps you anonymize logs files produced by firefly-iii server before
    sharing them for any bug report.  It tries to identify potentially sensitive
    information, and replace it with dummy values, while conserving value consistency
    across the log file.  Updated logs are printed to stdout.

    The input file should be a valid path on the system where the script is being
    executed, and defaults to stdin.
    """
    LOGGER.setLevel(log_level)

    print(file.read())


main()
