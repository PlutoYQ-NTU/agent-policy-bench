from agent_policy_bench.corpus import load_corpus
from agent_policy_bench.markdown import render_markdown_report
from agent_policy_bench.scoring import load_predictions, score_predictions


def test_score_predictions_reports_perfect_baseline():
    cases = load_corpus("corpus/shell_commands.yaml")
    predictions = load_predictions("examples/baseline_predictions.json")

    report = score_predictions(cases, predictions)

    assert report.risk_accuracy == 1.0
    assert report.false_allow == 0
    assert report.false_block == 0
    assert report.dangerous_miss_rate == 0.0
    assert report.credential_risk_miss_rate == 0.0


def test_score_predictions_detects_false_allow():
    cases = load_corpus("corpus/shell_commands.yaml")
    predictions = load_predictions("examples/baseline_predictions.json")
    predictions["dangerous_pipe_to_shell"] = predictions["dangerous_pipe_to_shell"].__class__(
        id="dangerous_pipe_to_shell",
        risk="read_only",
        decision="allow",
    )

    report = score_predictions(cases, predictions)

    assert report.false_allow == 1
    assert report.dangerous_miss_rate > 0


def test_markdown_report_contains_required_metrics():
    cases = load_corpus("corpus/shell_commands.yaml")
    predictions = load_predictions("examples/baseline_predictions.json")

    markdown = render_markdown_report(score_predictions(cases, predictions))

    assert "Risk-level accuracy" in markdown
    assert "False allow" in markdown
    assert "Dangerous miss rate" in markdown
