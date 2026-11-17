"""Synthetic outbox state-machine tests. Dm.Andreyanov / Prizolov Lab."""
import unittest
from telegram_outbox_contract import Event, State, transition


class OutboxTests(unittest.TestCase):
    def test_pending_claim_delivered(self):
        event = transition(Event("evt_00001"), "claim")
        self.assertEqual(event.attempts, 1)
        self.assertEqual(transition(event, "delivered", receipt="synthetic:42").state, State.DELIVERED)

    def test_delivery_requires_receipt(self):
        with self.assertRaisesRegex(ValueError, "missing_receipt"):
            transition(transition(Event("evt_00001"), "claim"), "delivered")

    def test_delivered_terminal(self):
        event = transition(transition(Event("evt_00001"), "claim"), "delivered", receipt="synthetic:42")
        with self.assertRaisesRegex(ValueError, "terminal_event"):
            transition(event, "claim")

    def test_failure_can_retry(self):
        event = transition(transition(Event("evt_00001"), "claim"), "failed")
        self.assertEqual(transition(event, "claim").attempts, 2)

    def test_exhaustion_dead_letter(self):
        event = Event("evt_00001")
        for _ in range(3):
            event = transition(transition(event, "claim"), "failed")
        self.assertEqual(event.state, State.DEAD)
        with self.assertRaisesRegex(ValueError, "terminal_event"):
            transition(event, "claim")

    def test_no_delivery_before_claim(self):
        with self.assertRaisesRegex(ValueError, "invalid_transition"):
            transition(Event("evt_00001"), "delivered", receipt="synthetic:42")


if __name__ == "__main__":
    unittest.main()
