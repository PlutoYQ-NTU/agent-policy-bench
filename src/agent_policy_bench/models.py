from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CommandCase:
    id: str
    command: str
    expected_risk: str
    expected_decision: str
    category: str = "custom"
    rationale: str = ""


@dataclass(frozen=True)
class Prediction:
    id: str
    risk: str
    decision: str


@dataclass(frozen=True)
class CommandScore:
    id: str
    command: str
    expected_risk: str
    predicted_risk: str
    expected_decision: str
    predicted_decision: str
    passed_risk: bool
    passed_decision: bool
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ScoreReport:
    total: int
    correct_risk: int
    risk_accuracy: float
    false_allow: int
    false_block: int
    dangerous_miss_rate: float
    credential_risk_miss_rate: float
    command_scores: list[CommandScore]
