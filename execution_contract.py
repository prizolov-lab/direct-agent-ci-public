# Author: Dm.Andreyanov | Brand: Prizolov Lab
# Product: Prizolov Yandex Direct Agent | public-contract v1.0.0
"""Strictly public, non-executable status contract. Never accepts client payloads."""
from __future__ import annotations

EVENTS = frozenset({"runner_ready", "execution_blocked", "review_required"})
FIELDS = frozenset({"schema", "event"})


def validate_public_event(obj: object) -> str:
    if not isinstance(obj, dict) or set(obj) != FIELDS:
        raise ValueError("public event must have exactly schema and event")
    if type(obj["schema"]) is not int or obj["schema"] != 1:
        raise ValueError("unsupported schema")
    if type(obj["event"]) is not str or obj["event"] not in EVENTS:
        raise ValueError("unsupported public event")
    return obj["event"]
