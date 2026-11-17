# Author: Dm.Andreyanov | Prizolov Lab | Prizolov Yandex Direct Agent
"""Public, dependency-free contract tests. No credentials or client data."""
import unittest
from execution_contract import validate_public_event


class ContractTests(unittest.TestCase):
    def test_allowed_health(self):
        self.assertEqual(validate_public_event({"schema": 1, "event": "runner_ready"}), "runner_ready")

    def test_allowed_blocked(self):
        self.assertEqual(validate_public_event({"schema": 1, "event": "execution_blocked"}), "execution_blocked")

    def test_reject_private_fields(self):
        for field in ("cmd", "token", "client", "account", "url", "text", "payload", "approval", "secret"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_public_event({"schema": 1, "event": "runner_ready", field: "private"})

    def test_reject_arbitrary_event(self):
        with self.assertRaises(ValueError):
            validate_public_event({"schema": 1, "event": "launch_campaign"})

    def test_reject_wrong_schema(self):
        with self.assertRaises(ValueError):
            validate_public_event({"schema": "1", "event": "runner_ready"})


if __name__ == "__main__":
    unittest.main()
