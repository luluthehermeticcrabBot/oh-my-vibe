"""Command-safety decision models and advisory analyzer composition."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass
from enum import StrEnum
import inspect
import logging
from typing import Protocol

logger = logging.getLogger(__name__)


class Decision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    SANDBOX = "sandbox"
    ASK = "ask"


@dataclass(frozen=True)
class CommandDecision:
    outcome: Decision
    reason: str
    evaluator: str
    sandbox_eligible: bool = False


class CommandAnalyzer(Protocol):
    def __call__(self, command: str) -> CommandDecision: ...


def evaluate_advisory_analyzers(
    command: str,
    analyzers: list[tuple[str, CommandAnalyzer]],
    *,
    timeout_seconds: float,
) -> list[CommandDecision]:
    """Evaluate analyzers; failures and timeouts become approval requests."""
    decisions: list[CommandDecision] = []
    for name, analyzer in analyzers:
        executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="omv-analyzer")
        future = executor.submit(analyzer, command)
        try:
            result = future.result(timeout=timeout_seconds)
            if inspect.isawaitable(result):
                raise TypeError(
                    "async analyzers are not supported by the sync policy path"
                )
            if not isinstance(result, CommandDecision):
                raise TypeError("analyzer returned an invalid decision")
            decisions.append(result)
        except TimeoutError:
            logger.warning("Oh My Vibe analyzer timed out: %s", name)
            return [
                CommandDecision(
                    Decision.ASK, f"advisory analyzer {name!r} timed out", name
                )
            ]
        except Exception as exc:
            logger.warning("Oh My Vibe analyzer failed: %s: %s", name, exc)
            return [
                CommandDecision(
                    Decision.ASK,
                    f"advisory analyzer {name!r} failed; human approval required",
                    name,
                )
            ]
        finally:
            executor.shutdown(wait=False, cancel_futures=True)
    return decisions


def combine_advisory_decisions(
    core: CommandDecision, advisory: list[CommandDecision]
) -> CommandDecision:
    """Combine untrusted plugin/LLM opinions without weakening core safety."""
    if core.outcome == Decision.DENY:
        return core
    if any(item.outcome == Decision.DENY for item in advisory):
        denied = next(item for item in advisory if item.outcome == Decision.DENY)
        return denied
    if any(item.outcome == Decision.ASK for item in advisory):
        ambiguous = next(item for item in advisory if item.outcome == Decision.ASK)
        return ambiguous
    if core.outcome == Decision.SANDBOX:
        return core
    if advisory and all(item.outcome == Decision.ALLOW for item in advisory):
        return CommandDecision(
            Decision.ALLOW,
            "All configured advisory analyzers classified the command as safe",
            "advisory-policy",
            sandbox_eligible=core.sandbox_eligible,
        )
    return core


def compose_policy_decision(
    core: CommandDecision,
    advisory: list[CommandDecision] | None = None,
    *,
    human_denied: bool = False,
) -> CommandDecision:
    """Apply deterministic, human, and advisory safety precedence."""
    if human_denied:
        return CommandDecision(Decision.DENY, "explicitly denied by the user", "human")
    return combine_advisory_decisions(core, advisory or [])
