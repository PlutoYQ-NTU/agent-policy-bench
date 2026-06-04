# agent-policy-bench

`agent-policy-bench` is a lightweight benchmark and test corpus for evaluating coding-agent command approval policies.

It scores predicted command risk and approval decisions against a small YAML corpus. The goal is to make policy regressions visible before a local coding-agent controller starts allowing risky commands or blocking routine inspection work.

This project is not a sandbox and does not execute commands.

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
python -m pytest
```

## Quick Start

Validate the bundled corpus:

```bash
agent-policy-bench validate --corpus corpus/shell_commands.yaml
```

Score predictions:

```bash
agent-policy-bench score \
  --corpus corpus/shell_commands.yaml \
  --predictions examples/baseline_predictions.json \
  --out reports/policy_report.md
```

## Prediction Format

Predictions can be a dictionary keyed by command id:

```json
{
  "safe_git_status": {"risk": "read_only", "decision": "allow"}
}
```

They can also be a list:

```json
[
  {"id": "safe_git_status", "risk": "read_only", "decision": "allow"}
]
```

If `decision` is omitted, the tool derives it from the predicted risk using the default mapping in `agent_policy_bench.scoring`.

## Metrics

The report includes:

- risk-level accuracy
- false allow count
- false block count
- dangerous miss rate
- credential-risk miss rate
- per-command classification table

## Limitations

- The bundled corpus is intentionally small and should be extended for each controller or shell environment.
- The tool scores labels; it does not judge whether a command is truly safe to execute.
- Shell aliases, scripts, environment variables, and platform-specific parsing can hide risk.

## Roadmap

See [ROADMAP.md](ROADMAP.md).
