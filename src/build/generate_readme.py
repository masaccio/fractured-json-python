"""Patch the README template with the most recent command-line help."""

import subprocess
from os import environ
from pathlib import Path
from typing import Final

MAX_COLUMNS = 76


def last_comma_after_pos(s: str, start: int) -> int:
    """Find index of last comma in s after a start position."""
    return s.rfind(",", start)


def main() -> None:
    docs_readme: Final[Path] = Path("docs/README.md")
    out_readme: Final[Path] = Path("README.md")

    environ["COLUMNS"] = str(MAX_COLUMNS)
    result = subprocess.run(
        ["fractured-json", "--help"],  # noqa: S607
        check=True,
        capture_output=True,
        text=True,
    )

    help_text = ""
    for line in result.stdout.splitlines():
        if len(line) > MAX_COLUMNS and "{" in line:
            # argparse doesn't break choices across lines so
            # find the last fitting choice and insert a bread
            # padding the next line to line up to the brace position
            choice_start = line.find("{") + 1
            choice_break = line.rfind(",", choice_start, MAX_COLUMNS + 1) + 1
            help_text += line[:choice_break] + "\n"
            help_text += " " * choice_start
            help_text += line[choice_break:] + "\n"
        else:
            help_text += line + "\n"

    text = docs_readme.read_text(encoding="utf-8")

    marker = "__COMMAND_LINE_HELP__\n"
    if marker not in text:
        msg = f"Marker {marker!r} not found in {docs_readme}"
        raise RuntimeError(msg)

    if not help_text.endswith("\n"):
        help_text += "\n"
    new_text = text.replace(marker, help_text)

    out_readme.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    main()
