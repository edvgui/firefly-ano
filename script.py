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
import itertools
import logging
import re
import sys
from collections.abc import Iterable, Iterator

import click
import click_loglevel

LOGGER = logging.getLogger()
logging.root.addHandler(logging.StreamHandler(sys.stderr))

AMOUNT = re.compile(r"(?P<amount>\"[-]?[0-9]+\.[0-9]+\")")
EMAIL = re.compile(r"(?P<email>[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+)")
ACCOUNT = re.compile(r"searchAccount\(\"(?P<account>[^\"]+)\"")
IBAN = re.compile(r"(?P<iban>[A-Z]{2}\d{2}[A-Z0-9]{10,30})[^A-Z0-9]?")
ASSET_ACCOUNT = re.compile(
    r"ID: Found Asset account account #\d+ \(\"(?P<account>[^\"]+)\""
)
ACCOUNT_VALIDATOR = re.compile(
    r"Now in AccountValidator::validateDestination\(\) "
    r"\{\"id\":[^,]+,\"name\":\"(?P<account>[^\"]+)\""
)
ORIGINAL_ACCOUNT = re.compile(r"\"Original account name: (?P<account>[^\"\\]+)\\?\"")


def find_sensitive_data(lines: Iterable[str], data: dict[str, str]) -> dict[str, str]:
    """
    Go over all the lines, and search for sensitive data.  Add all the
    sensitive data to a dict which provides an alternative value for the
    sensitive data.  Returns the mapping of sensitive data to alternative
    data.

    :param lines: The set of lines that should be searched for sensitive data.
    """
    account_id = iter(range(1_000_000))
    email_id = iter(range(1_000_000))
    iban_id = iter(range(1_000_000))

    for line in lines:

        # Search for an amount to anonymize
        for amount in AMOUNT.finditer(line):
            secret_amount = amount.group("amount")
            if secret_amount not in data:
                redacted_amount = '"0.0"'
                data[secret_amount] = redacted_amount
                LOGGER.debug(
                    "Amount %s will be replaced by %s", secret_amount, redacted_amount
                )

        # Search for account to anonymize
        for account in itertools.chain(
            ACCOUNT.finditer(line),
            ASSET_ACCOUNT.finditer(line),
            ACCOUNT_VALIDATOR.finditer(line),
            ORIGINAL_ACCOUNT.finditer(line),
        ):
            secret_account = account.group("account")
            if secret_account not in data:
                redacted_account = f"ACCOUNT{next(account_id)}"
                data[secret_account] = redacted_account
                LOGGER.debug(
                    "Account %s will be replaced by %s",
                    secret_account,
                    redacted_account,
                )

        # Search for email to anonymize
        for email in EMAIL.finditer(line):
            secret_email = email.group("email")
            if secret_email not in data:
                redacted_email = f"user{next(email_id)}@example.com"
                data[secret_email] = redacted_email
                LOGGER.debug(
                    "Email %s will be replaced by %s", secret_email, redacted_email
                )

        # Search for ibans to anonymize
        for iban in IBAN.finditer(line):
            secret_iban = iban.group("iban")
            if secret_iban not in data:
                redacted_iban = f"AA00{next(iban_id):015}"
                data[secret_iban] = redacted_iban
                LOGGER.debug(
                    "IBAN %s will be replaced by %s", secret_iban, redacted_iban
                )

    return data


def replace_sensitive_data(lines: Iterable[str], data: dict[str, str]) -> Iterator[str]:
    """
    Go over each line of the file, and replace any sensitive content that is
    part of the data dict, by its anonymized replacement.

    :param lines: The set of lines that should be anonymized.
    :param data: The mapping of secret to redacted data.
    """
    for line in lines:
        for old, new in data.items():
            line = line.replace(old, new)
        yield line


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
@click.option(
    "-e",
    "--extra",
    type=(str, str),
    help="Additional sensitive data to search and replace.",
    envvar="EXTRA",
    multiple=True,
)
@click.argument(
    "file",
    type=click.File("r"),
    default=sys.stdin,
    nargs=1,
    envvar="FILE",
)
def main(log_level: int, extra: list[tuple[str, str]], file: io.TextIOWrapper) -> None:
    """
    This tool helps you anonymize logs files produced by firefly-iii server before
    sharing them for any bug report.  It tries to identify potentially sensitive
    information, and replace it with dummy values, while conserving value consistency
    across the log file.  Updated logs are printed to stdout.

    The input file should be a valid path on the system where the script is being
    executed, and defaults to stdin.
    """
    LOGGER.setLevel(log_level)

    data: dict[str, str] = {}
    # Preload the data dict with the extra input from the user
    for secret, redacted in extra:
        if secret not in data:
            data[secret] = redacted
            LOGGER.debug("Value %s will be replaced by %s", secret, redacted)

    if not file.seekable():
        # Load the full file in memory so we go through the lines a second time
        lines = list(file)
    else:
        lines = iter(file)

    # Find the sensitive data in the document
    data = find_sensitive_data(lines, data)

    # Replace the sensitive data and print it to stdout
    if file.seekable():
        file.seek(0)
        lines = iter(file)

    for line in replace_sensitive_data(lines, data):
        print(line[:-1])


main()
