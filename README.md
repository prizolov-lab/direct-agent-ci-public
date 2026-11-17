# Prizolov Yandex Direct Agent — Public CI Harness

Author: **Dm.Andreyanov** · Brand: **Prizolov Lab** · Product: **Prizolov Yandex Direct Agent** · Version: **public-ci 0.1.0**

This is a standalone synthetic test harness, not the proprietary agent implementation. No access to private repositories, customer data, billing, credentials, or Yandex APIs. Passing these tests **does not validate** private `direct-agent` PR #1. Private release tests remain mandatory.

Run: `python -m unittest discover -s tests -v`.

Before adding any real code or data, audit contents and history for secrets, personal data, confidential algorithms and licenses.

## Verified CI status (2026-11-16)

The public GitHub Actions run [43886295911](https://github.com/prizolov-lab/direct-agent-ci-public/actions/runs/43886295911) completed successfully on Python 3.10 and Python 3.12. This evidence applies **only** to the synthetic `security_contract.py` reference and its tests, not to the proprietary implementation in `prizolov-lab/direct-agent` or its Draft PR #1.

A safe validation path for private code is to run the actual private test suite on a trusted machine, then record the exact commit SHA and sanitized test summary in the private PR. Do not publish private source code, CI artifacts containing proprietary code, credentials, or customer data in this repository. Passing synthetic tests must never satisfy private release gates by itself.



## Production execution boundary — 2026-11-17

Private run `prizolov-lab/direct-agent-data/actions/runs/44160601303` was refused before any step due to
GitHub account billing/spending limits. This public repository cannot remove that private execution restriction.
Do not dispatch production bot commands, supply Telegram tokens, checkout private repositories or pass real
notification text to public workflows. Public workflow inputs/logs must never become an alternate private outbox.

The private agent change provides `tools/owner_notify.py` and an explicit `cloud_dispatch.py --executor owner-local`
for a trusted private machine, using the existing bot and verified owner registry. It does not change the Worker,
KV or webhook. A delivery receipt requires a positive Telegram message ID. Unknown network outcomes are not
retried automatically. Activation and actual private test evidence belong in the private repository.

`tests/test_public_execution_boundary.py` checks the real public workflow for secret references, private checkout,
write permissions and unexpected shell commands. This is a public workflow boundary check, not a live delivery test.
