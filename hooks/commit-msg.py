#!/usr/bin/env python3
"""Git commit-msg hook that strips AI attribution from commit messages.

Removes AI co-author trailers (Co-Authored-By: Claude ..., Assisted-by: ...)
and "Generated with ..." footers, then writes the cleaned message back.
The subject line is never touched, so commits about AI features stay intact.
"""

import re
import sys

AI = re.compile(
    r"claude|anthropic|openai|chatgpt|\bgpt-?\d|copilot|gemini|cursor|codex"
    r"|aider|devin|windsurf|codeium|tabnine|\bllm\b|\bai\b|\[bot\]",
    re.IGNORECASE,
)

TRAILER = re.compile(
    r"^\s*(co-authored-by|assisted-by|generated-by|ai-assisted|ai-generated"
    r"|written-by|helped-by|made-with|signed-off-by)\s*:(?P<value>.*)$",
    re.IGNORECASE,
)

FOOTER = re.compile(r"^\W*generated (with|by)\b(?P<value>.*)$", re.IGNORECASE)

SCISSORS = re.compile(r"^# -+ >8 -+$")


def is_attribution(line: str) -> bool:
    for pattern in (TRAILER, FOOTER):
        match = pattern.match(line)
        if match and AI.search(match.group("value")):
            return True
    return False


def clean(message: str) -> tuple[str, list[str]]:
    lines = message.splitlines()

    # Leave the diff below the scissors line of `git commit -v` alone.
    end = next((i for i, line in enumerate(lines) if SCISSORS.match(line)), len(lines))
    body, rest = lines[:end], lines[end:]

    removed = []
    kept = body[:1]
    for line in body[1:]:
        if is_attribution(line):
            removed.append(line.strip())
        else:
            kept.append(line)

    # Drop blank lines left behind by removed trailers.
    while len(kept) > 1 and not kept[-1].strip():
        kept.pop()

    result = "\n".join(kept + ([""] if rest else []) + rest) + "\n"
    return result, removed


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: commit-msg <commit-message-file>", file=sys.stderr)
        return 1

    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        message = f.read()

    cleaned, removed = clean(message)
    if not removed:
        return 0

    with open(path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    for line in removed:
        print(f"commit-msg: removed AI attribution: {line}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
