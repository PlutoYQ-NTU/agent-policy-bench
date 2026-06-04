from __future__ import annotations

from pathlib import Path

from .models import CommandCase


REQUIRED_FIELDS = {"id", "command", "expected_risk", "expected_decision"}


def load_corpus(path: str | Path) -> list[CommandCase]:
    """Load the project's simple YAML command corpus format."""
    text = Path(path).read_text(encoding="utf-8")
    raw_items = _parse_simple_yaml_list(text)
    cases: list[CommandCase] = []
    seen: set[str] = set()
    for index, item in enumerate(raw_items, 1):
        missing = REQUIRED_FIELDS - set(item)
        if missing:
            raise ValueError(f"case #{index} missing required field(s): {', '.join(sorted(missing))}")
        case_id = item["id"]
        if case_id in seen:
            raise ValueError(f"duplicate case id: {case_id}")
        seen.add(case_id)
        cases.append(
            CommandCase(
                id=case_id,
                command=item["command"],
                expected_risk=item["expected_risk"],
                expected_decision=item["expected_decision"],
                category=item.get("category", "custom"),
                rationale=item.get("rationale", ""),
            )
        )
    return cases


def _parse_simple_yaml_list(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line == "commands:":
            continue
        if line.startswith("- "):
            if current is not None:
                items.append(current)
            current = {}
            line = line[2:].strip()
            if line:
                key, value = _split_key_value(line)
                current[key] = value
            continue
        if current is None:
            raise ValueError(f"unexpected line before first item: {raw_line}")
        key, value = _split_key_value(line)
        current[key] = value
    if current is not None:
        items.append(current)
    return items


def _split_key_value(line: str) -> tuple[str, str]:
    if ":" not in line:
        raise ValueError(f"expected key: value line, got: {line}")
    key, value = line.split(":", 1)
    return key.strip(), _unquote(value.strip())


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value
