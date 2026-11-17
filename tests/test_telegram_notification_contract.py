"""Standalone public routing contract tests.

Author: Dm.Andreyanov | Prizolov Lab
Product: Prizolov Yandex Direct Agent | public-ci 0.2.0
"""
import unittest
from telegram_notification_contract import route_notification

VALID = {"event_id": "event_000001", "role": "checker", "audience": "owner", "text": "Synthetic test"}


class TelegramNotificationContractTests(unittest.TestCase):
    def test_owner_allowed(self):
        d = route_notification(VALID, {"synthetic-owner": "owner"})
        self.assertTrue(d.allowed)
        self.assertEqual(d.destination, "synthetic-owner")

    def test_no_owner_denied(self):
        self.assertEqual(route_notification(VALID, {}).reason, "owner_binding_not_unique")

    def test_ambiguous_owner_denied(self):
        bindings = {"owner_a": "owner", "owner_b": "owner"}
        self.assertFalse(route_notification(VALID, bindings).allowed)

    def test_invalid_role_denied(self):
        self.assertFalse(route_notification({**VALID, "role": "unknown"}, {"o": "owner"}).allowed)

    def test_invalid_event_id_denied(self):
        self.assertFalse(route_notification({**VALID, "event_id": "x"}, {"o": "owner"}).allowed)

    def test_empty_body_denied(self):
        self.assertFalse(route_notification({**VALID, "text": " "}, {"o": "owner"}).allowed)

    def test_client_claimed_approval_denied(self):
        msg = {**VALID, "audience": "client", "client_approved": True, "folder": "example.test"}
        d = route_notification(msg, {"o": "owner"})
        self.assertEqual(d.reason, "client_delivery_not_enabled")

    def test_caller_chat_id_not_used(self):
        d = route_notification({**VALID, "chat_id": "attacker"}, {"o": "owner"})
        self.assertEqual(d.destination, "o")

if __name__ == "__main__":
    unittest.main()
