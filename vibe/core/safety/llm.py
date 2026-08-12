"""Provider-neutral advisory LLM command analyzer boundary."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from vibe.core.safety.policy import CommandDecision, Decision

LLMClassification = Decision | str | Mapping[str, object]


class LLMCommandClassifier(Protocol):
    def __call__(self, command: str) -> LLMClassification: ...


class LLMAnalyzer:
    """Adapt an injected classifier into the advisory command-analyzer contract."""

    def __init__(
        self, classifier: LLMCommandClassifier, *, evaluator: str = "llm"
    ) -> None:
        if not evaluator.strip():
            raise ValueError("evaluator cannot be empty")
        self._classifier = classifier
        self._evaluator = evaluator

    def __call__(self, command: str) -> CommandDecision:
        classification = self._classifier(command)
        outcome, reason = self._parse_classification(classification)
        return CommandDecision(outcome, reason, self._evaluator)

    def _parse_classification(
        self, classification: LLMClassification
    ) -> tuple[Decision, str]:
        if isinstance(classification, Decision):
            return classification, f"LLM classified command as {classification.value}"
        if isinstance(classification, str):
            value = classification.strip().lower()
            reason = f"LLM classified command as {value}"
        elif isinstance(classification, Mapping):
            raw_outcome = classification.get("decision", classification.get("outcome"))
            if not isinstance(raw_outcome, str):
                raise ValueError("LLM classification must include a string decision")
            value = raw_outcome.strip().lower()
            raw_reason = classification.get("reason")
            reason = raw_reason.strip() if isinstance(raw_reason, str) else ""
            reason = reason or f"LLM classified command as {value}"
        else:
            raise TypeError("LLM classifier returned an unsupported classification")

        try:
            outcome = Decision(value)
        except ValueError as exc:
            raise ValueError(f"unsupported LLM decision: {value!r}") from exc
        if outcome == Decision.SANDBOX:
            raise ValueError("LLM analyzers cannot select sandbox execution")
        return outcome, reason


__all__ = ["LLMAnalyzer", "LLMClassification", "LLMCommandClassifier"]
