# firefly-ano

[Firefly III](https://github.com/firefly-iii/) is an amazing tool to manage personal finances.

This script allows you to more easily anonymize logs produced by the firefly-iii server when sharing them to report an issue.

The script works as follows:
1. Read the logs a first time, try to recognize any data format or log lines which are known to contain sensitive data.
2. Parse the sensitive data in these lines, and come up with an alternative value for the sensitive data.
3. Read the logs a second time, replace in each line any value matching any of the sensitive data that was resolved before, and print the line to stdout.

You can also provide extra values that you know should be redacted but the script doesn't handle yet using the `--extra <secret> <redacted>` argument.

## Disclaimer

There is absolutely no guarantee that the script will find and replace every sensitive data contained in the logs.  I do not recommend publishing the outgoing anonymized logs anywhere online.

## Run from source

**Requirements**:
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

```console
$ git clone https://github.com/edvgui/firefly-ano.git
Usage: script.py [OPTIONS] [FILE]

  This tool helps you anonymize logs files produced by firefly-iii server
  before sharing them for any bug report.  It tries to identify potentially
  sensitive information, and replace it with dummy values, while conserving
  value consistency across the log file.  Updated logs are printed to stdout.

  The input file should be a valid path on the system where the script is
  being executed, and defaults to stdin.

Options:
  -l, --log-level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Set logging level  [env var: LOG_LEVEL;
                                  default: INFO]
  -e, --extra <TEXT TEXT>...      Additional sensitive data to search and
                                  replace.
  --help                          Show this message and exit.
$ echo '$$$' | ./script.py --log-level debug --extra $ €
Value $ will be replaced by €
€€€
```

## Run with podman

**Requirements**:
- podman or docker

```console
$ podman run --rm -i ghcr.io/edvgui/firefly-ano:latest --help
Usage: script.py [OPTIONS] [FILE]

  This tool helps you anonymize logs files produced by firefly-iii server
  before sharing them for any bug report.  It tries to identify potentially
  sensitive information, and replace it with dummy values, while conserving
  value consistency across the log file.  Updated logs are printed to stdout.

  The input file should be a valid path on the system where the script is
  being executed, and defaults to stdin.

Options:
  -l, --log-level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Set logging level  [env var: LOG_LEVEL;
                                  default: INFO]
  --help                          Show this message and exit.
$ podman run --rm -i ghcr.io/edvgui/firefly-ano:latest < original.log > modified.log
```

## Options

All options can be provided via cli or environment variables, when both are used, the value provided via cli takes precedence.

| Option | Env var | Description |
| --- | --- | --- |
| `-l/--log-level` | `LOG_LEVEL` | The log level of the script. |
| `-e/--extra` | `EXTRA` | Extra values to redact and replace. |
| `<file>` | `FILE` | The path to the log file that should be anonymized. |
