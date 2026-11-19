# Author — Dm.Andreyanov | Brand — Prizolov Lab
# Product — Prizolov Yandex Direct Agent | public-owner-notify tests v1.0.0
import io
import json
from pathlib import Path
import unittest
from unittest import mock
import urllib.error
import telegram_owner_sender as sender


class OwnerSenderTests(unittest.TestCase):
    def env(self):
        return {"GITHUB_REPOSITORY": sender.REPO, "GITHUB_REF": "refs/heads/main",
                "GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_ACTOR": sender.ACTOR,
                "GITHUB_RUN_ATTEMPT": "1", "TELEGRAM_BOT_TOKEN": "123:" + "fake" * 10,
                "TELEGRAM_OWNER_CHAT_ID": "123", "NOTICE_EVENT": "test"}

    def opener(self, payload):
        opener = mock.Mock()
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(payload).encode()
        opener.open.return_value = response
        return opener

    def test_success_requires_positive_message_id_and_owner(self):
        opener = self.opener({"ok": True, "result": {"message_id": 42, "chat": {"id": 123}}})
        self.assertEqual(sender.send(self.env(), opener), {"status": "delivered", "message_id": 42})
        request = opener.open.call_args.args[0]
        body = json.loads(request.data)
        self.assertEqual(body["chat_id"], "123")
        self.assertIn("Prizolov Yandex Direct Agent", body["text"])
        self.assertNotIn("Доктор ПУХ", body["text"])
        self.assertNotIn("parse_mode", body)

    def test_evidence_event_has_no_approval(self):
        env = self.env()
        env["NOTICE_EVENT"] = "evidence_summary_ready"
        opener = self.opener({"ok": True, "result": {"message_id": 43, "chat": {"id": 123}}})
        self.assertEqual(sender.send(env, opener)["status"], "delivered")
        body = json.loads(opener.open.call_args.args[0].data)
        self.assertIn("Рекламные действия запрещены", body["text"])
        self.assertNotIn("klin.doctor-puh.ru", body["text"])

    def test_all_fixed_events_are_supported(self):
        for event in sender.MESSAGES:
            env = self.env()
            env["NOTICE_EVENT"] = event
            self.assertIsNone(sender.preflight(env))

    def test_missing_secrets_block_before_network(self):
        for field in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_OWNER_CHAT_ID"):
            env = self.env()
            del env[field]
            opener = mock.Mock()
            self.assertTrue(sender.send(env, opener)["status"].startswith("blocked_"))
            opener.open.assert_not_called()

    def test_untrusted_context_and_rerun_block_before_network(self):
        changes = {"GITHUB_REPOSITORY": "fork/repo", "GITHUB_REF": "refs/heads/other",
                   "GITHUB_EVENT_NAME": "pull_request", "GITHUB_ACTOR": "other", "GITHUB_RUN_ATTEMPT": "2"}
        for key, value in changes.items():
            env = self.env()
            env[key] = value
            opener = mock.Mock()
            self.assertEqual(sender.send(env, opener)["status"], "blocked_untrusted_context")
            opener.open.assert_not_called()

    def test_free_text_event_is_rejected(self):
        env = self.env()
        env["NOTICE_EVENT"] = "client private report"
        self.assertEqual(sender.send(env, mock.Mock())["status"], "blocked_unknown_event")

    def test_invalid_receipts_are_unknown(self):
        for payload in ([], {"ok": True}, {"ok": True, "result": []},
                        {"ok": True, "result": {"message_id": True, "chat": {"id": 123}}},
                        {"ok": True, "result": {"message_id": 42, "chat": {"id": 456}}}):
            with self.subTest(payload=payload):
                self.assertEqual(sender.send(self.env(), self.opener(payload))["status"], "unknown_no_automatic_retry")

    def test_timeout_does_not_leak_token_or_retry(self):
        opener = mock.Mock()
        opener.open.side_effect = OSError("secret URL must not be printed")
        result = sender.send(self.env(), opener)
        self.assertEqual(result, {"status": "unknown_no_automatic_retry"})
        self.assertEqual(opener.open.call_count, 1)

    def test_explicit_telegram_rejection(self):
        opener = self.opener({"ok": False, "description": "private"})
        self.assertEqual(sender.send(self.env(), opener), {"status": "telegram_rejected"})
        opener.open.side_effect = urllib.error.HTTPError("secret", 400, "", {}, io.BytesIO(b'{"ok":false}'))
        self.assertEqual(sender.send(self.env(), opener), {"status": "telegram_rejected"})

    def test_sender_workflow_has_no_pr_trigger_or_private_checkout(self):
        source = (Path(__file__).resolve().parents[1] / ".github/workflows/telegram-owner.yml").read_text()
        for forbidden in ("pull_request:", "schedule:", "pull_request_target:", "direct-agent-data",
                          "AGENT_REPO_TOKEN", "actions: write", "contents: write"):
            self.assertNotIn(forbidden, source)
        self.assertIn("workflow_dispatch:", source)
        self.assertIn("branches: [main]", source)
        self.assertIn("notifications/owner/*.json", source)
        self.assertIn("github.run_attempt == 1", source)
        self.assertIn("persist-credentials: false", source)
        self.assertNotIn("${{ inputs.event }}", source.split("run:")[-1])


class PushMarkerTests(unittest.TestCase):
    def test_only_new_fixed_event_marker_is_accepted(self):
        env = {"NOTICE_BEFORE": "a" * 40, "GITHUB_SHA": "b" * 40}
        diff = mock.Mock(stdout="A\tnotifications/owner/test_0001.json\n")
        with mock.patch.object(sender.subprocess, "run", return_value=diff), \
                mock.patch.object(sender.Path, "is_symlink", return_value=False), \
                mock.patch.object(sender.Path, "stat", return_value=mock.Mock(st_size=30)), \
                mock.patch.object(sender.Path, "read_text", return_value='{"event":"test"}'):
            self.assertEqual(sender.push_event(env), "test")
            with mock.patch.object(sender.Path, "read_text", return_value='{"event":"test","text":"private"}'):
                with self.assertRaises(ValueError):
                    sender.push_event(env)
            diff.stdout = "M\tnotifications/owner/test_0001.json\n"
            with self.assertRaises(ValueError):
                sender.push_event(env)

    def test_bad_commit_is_blocked_before_git(self):
        with mock.patch.object(sender.subprocess, "run") as run:
            with self.assertRaises(ValueError):
                sender.push_event({"NOTICE_BEFORE": "--invalid", "GITHUB_SHA": "b" * 40})
            run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
