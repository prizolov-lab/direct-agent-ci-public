"""Public synthetic Telegram routing contract — no private bot code.

Author: Dm.Andreyanov
Brand: Prizolov Lab
Product: Prizolov Yandex Direct Agent
Version: public-ci 0.2.0
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any

ROLES = frozenset({"orchestrator", "chief_executor", "executor", "assistant", "checker", "monitor"})
ID_PATTERN = __import__("re").compile(r"^[A-Za-z0-9_-]{8,100}$")
FOLDER_PATTERN = __import__("re").compile(r"^[A-Za-z0-9._-]{1,120}$")


@dataclass(frozen=True)
class Decision:
    allowed: bool
    destination: str | None = None
    reason: str = ""


def route_notification(message: Mapping[str, Any], bindings: Mapping[str, Any]) -> Decision:
    """Validate a public-only model contract, not the deployed/private implementation.

    Deliberate fail-closed behavior: caller-asserted approval is insufficient for clients.
    No network, no credentials, no customer account identifiers, no external dispatch.
    """
    event_id = message.get("event_id")
    role = message.get("role")
    audience = message.get("audience")
    body = message.get("text")
    if (role not in ROLES or audience not in {"owner", "client"}
            or not isinstance(event_id, str) or not ID_PATTERN.fullmatch(event_id)
            or not isinstance(body, str) or not body.strip() or len(body) > 3500):
        return Decision(False, reason="invalid_payload")
    if audience == "client":
        return Decision(False, reason="client_delivery_not_enabled")
    owners = [ident for ident, role_name in bindings.items() if role_name == "owner"]
    if len(owners) != 1:
        return Decision(False, reason="owner_binding_not_unique")
    return Decision(True, destination=str(owners[0]))
