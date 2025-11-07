# firefly-ano

[Firefly III](https://github.com/firefly-iii/) is an amazing tool to manage personal finances.

TODO

## Run from source

**Requirements**:
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

```console
$ git clone https://github.com/edvgui/firefly-ano.git
$ ./script.py --help
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
$ ./script.py < original.log > modified.log
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
| `<file>` | `File` | The path to the log file that should be anonymized. |
