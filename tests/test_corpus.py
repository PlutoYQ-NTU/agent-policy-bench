from pathlib import Path

import pytest

from agent_policy_bench.corpus import load_corpus


def test_load_corpus_reads_command_cases():
    cases = load_corpus("corpus/shell_commands.yaml")

    assert len(cases) >= 10
    assert cases[0].id == "safe_git_status"
    assert cases[0].expected_decision == "allow"


def test_load_corpus_rejects_duplicate_ids(tmp_path: Path):
    corpus = tmp_path / "corpus.yaml"
    corpus.write_text(
        """commands:
  - id: duplicate
    command: "git status"
    expected_risk: read_only
    expected_decision: allow
  - id: duplicate
    command: "git diff"
    expected_risk: read_only
    expected_decision: allow
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate"):
        load_corpus(corpus)
