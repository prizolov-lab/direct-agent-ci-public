# Author — Dm.Andreyanov | Brand — Prizolov Lab
# Product — Prizolov Yandex Direct Agent | public-ci boundary v0.1
"""Check the actual public workflow, not a hypothetical sender contract."""
from pathlib import Path
import re
import unittest


class PublicExecutionBoundary(unittest.TestCase):
    def test_every_public_workflow_remains_secret_free_and_synthetic(self):
        workflows = list((Path(__file__).resolve().parents[1] / ".github" / "workflows").glob("*.y*ml"))
        self.assertTrue(workflows)
        for path in workflows:
            source = path.read_text(encoding="utf-8")
            with self.subTest(workflow=path.name):
                for forbidden in (r"secrets\s*[.\[]", r"pull_request_target\s*:", r"workflow_run\s*:",
                                  r"repository\s*:", r"persist-credentials\s*:\s*true", r"contents\s*:\s*write",
                                  r"actions\s*:\s*write", r"api\.telegram\.org", r"direct-agent-data",
                                  r"TELEGRAM_BOT_TOKEN", r"AGENT_REPO_TOKEN"):
                    self.assertIsNone(re.search(forbidden, source, re.I), forbidden)
                self.assertIn("contents: read", source)
                # Restrict all shell steps to the reviewed dependency-free synthetic suite.
                commands = re.findall(r"^\s*run:\s*(.+)$", source, re.M)
                self.assertEqual(commands, ["python -m unittest discover -s tests -v"])


if __name__ == "__main__":
    unittest.main()
