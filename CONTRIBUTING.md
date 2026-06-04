# Contributing

Keep this benchmark small, transparent, and dependency-light.

## Development

```bash
pip install -e ".[dev]"
python -m pytest
```

## Corpus Changes

When adding commands:

- Use synthetic examples only.
- Do not include real secrets, private paths, or organization-specific commands.
- Include expected `risk`, expected `decision`, and a short rationale.
- Add tests when changing corpus parsing or scoring behavior.

## Policy Labels

Supported risk labels are:

- `read_only`
- `write_workspace`
- `run_expensive`
- `network`
- `delete`
- `credential_risk`
- `dangerous`
- `unknown`

Supported decisions are:

- `allow`
- `require_approval`
- `block`
