from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .corpus import load_corpus
from .markdown import render_markdown_report
from .scoring import load_predictions, score_predictions


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        cases = load_corpus(args.corpus)
    except (OSError, ValueError) as exc:
        print(f"validate error: {exc}", file=sys.stderr)
        return 2
    print(f"Corpus valid: {len(cases)} command case(s)")
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    try:
        cases = load_corpus(args.corpus)
        predictions = load_predictions(args.predictions)
        report = score_predictions(cases, predictions)
    except (OSError, ValueError) as exc:
        print(f"score error: {exc}", file=sys.stderr)
        return 2
    rendered = render_markdown_report(report)
    if args.out:
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Wrote policy report to {output_path}")
    else:
        print(rendered, end="")
    return 1 if args.fail_on_false_allow and report.false_allow > 0 else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-policy-bench", description="Score coding-agent command approval policy predictions.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate a command corpus.")
    validate.add_argument("--corpus", required=True, help="Command corpus YAML path.")
    validate.set_defaults(func=cmd_validate)

    score = subparsers.add_parser("score", help="Score predictions against a command corpus.")
    score.add_argument("--corpus", required=True, help="Command corpus YAML path.")
    score.add_argument("--predictions", required=True, help="Prediction JSON path.")
    score.add_argument("--out", help="Optional Markdown report output path.")
    score.add_argument("--fail-on-false-allow", action="store_true", help="Return nonzero if any false allow is detected.")
    score.set_defaults(func=cmd_score)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
