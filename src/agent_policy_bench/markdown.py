from __future__ import annotations

from .models import ScoreReport


def render_markdown_report(report: ScoreReport) -> str:
    lines = [
        "# Agent Policy Bench Report",
        "",
        "## Summary",
        "",
        f"- Total commands: {report.total}",
        f"- Risk-level accuracy: {report.risk_accuracy:.1%}",
        f"- Correct risk labels: {report.correct_risk}",
        f"- False allow: {report.false_allow}",
        f"- False block: {report.false_block}",
        f"- Dangerous miss rate: {report.dangerous_miss_rate:.1%}",
        f"- Credential-risk miss rate: {report.credential_risk_miss_rate:.1%}",
        "",
        "## Per-Command Classification",
        "",
        "| ID | Expected Risk | Predicted Risk | Expected Decision | Predicted Decision | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for score in report.command_scores:
        notes = ", ".join(score.notes) if score.notes else ""
        lines.append(
            "| "
            f"{score.id} | {score.expected_risk} | {score.predicted_risk} | "
            f"{score.expected_decision} | {score.predicted_decision} | {notes} |"
        )
    lines.append("")
    return "\n".join(lines)
