from pathlib import Path

from agent_policy_bench import cli


def test_validate_cli_accepts_bundled_corpus(capsys):
    code = cli.main(["validate", "--corpus", "corpus/shell_commands.yaml"])

    captured = capsys.readouterr()
    assert code == 0
    assert "Corpus valid" in captured.out


def test_score_cli_writes_report(tmp_path: Path):
    output = tmp_path / "report.md"

    code = cli.main(
        [
            "score",
            "--corpus",
            "corpus/shell_commands.yaml",
            "--predictions",
            "examples/baseline_predictions.json",
            "--out",
            str(output),
        ]
    )

    assert code == 0
    assert "Risk-level accuracy" in output.read_text(encoding="utf-8")
