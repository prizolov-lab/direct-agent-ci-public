"""Pure synthetic notification outbox state-machine contract.

Author: Dm.Andreyanov | Prizolov Lab
Product: Prizolov Yandex Direct Agent | public-ci 0.3.0

This is NOT a production queue: the caller must provide atomic transactions
and persistent storage in its own trusted infrastructure.
"""
from dataclasses import dataclass
from enum import Enum


class State(str, Enum):
    PENDING = "pending"
    CLAIMED = "claimed"
    DELIVERED = "delivered"
    FAILED = "failed"
    DEAD = "dead"


@dataclass(frozen=True)
class Event:
    event_id: str
    state: State = State.PENDING
    attempts: int = 0
    receipt: str | None = None


def transition(event: Event, action: str, *, receipt: str | None = None, max_attempts: int = 3) -> Event:
    """Model allowed transitions; caller must serialize operations atomically."""
    if event.state in {State.DELIVERED, State.DEAD}:
        raise ValueError("terminal_event")
    if action == "claim" and event.state in {State.PENDING, State.FAILED}:
        if event.attempts >= max_attempts:
            raise ValueError("retry_exhausted")
        return Event(event.event_id, State.CLAIMED, event.attempts + 1)
    if action == "delivered" and event.state == State.CLAIMED:
        if not receipt:
            raise ValueError("missing_receipt")
        return Event(event.event_id, State.DELIVERED, event.attempts, receipt)
    if action == "failed" and event.state == State.CLAIMED:
        return Event(event.event_id, State.DEAD if event.attempts >= max_attempts else State.FAILED, event.attempts)
    raise ValueError("invalid_transition")
