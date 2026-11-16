# Prizolov Yandex Direct Agent — Public CI Harness

Author: **Dm.Andreyanov** · Brand: **Prizolov Lab** · Product: **Prizolov Yandex Direct Agent** · Version: **public-ci 0.1.0**

This is a standalone synthetic test harness, not the proprietary agent implementation. No access to private repositories, customer data, billing, credentials, or Yandex APIs. Passing these tests **does not validate** private `direct-agent` PR #1. Private release tests remain mandatory.

Run: `python -m unittest discover -s tests -v`.

Before adding any real code or data, audit contents and history for secrets, personal data, confidential algorithms and licenses.
