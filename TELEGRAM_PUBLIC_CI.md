# Telegram notification public CI, v0.2.0

Author: **Dm.Andreyanov** · Brand: **Prizolov Lab** · Product: **Prizolov Yandex Direct Agent**

## Purpose

Use this existing **public synthetic CI** to validate a dependency-free routing/security contract for owner notifications. `public-ci.yml` discovers `tests/test_telegram_notification_contract.py` on Python 3.10 and 3.12 automatically. No changes to workflow permissions, access tokens, or checkout configuration.

The tests check routing to exactly one synthetic owner, refusal of missing/ambiguous owner, unknown role, malformed event ID, empty message, spoofed chat ID, and **client notifications disabled pending verifiable authorization**.

## Safe trust boundary

- Public repository: synthetic contract and tests only.
- Private `direct-agent`: actual Telegram Worker changes, separate draft PR #4, actual source tests.
- Private `direct-agent-data`: real projects and delivery receipts; never imported into public CI.
- Cloudflare Worker: live Telegram interface; no deployment from this public CI.
- Public green checks mean **synthetic behavior is correct**, not that the private agent is deployed or Telegram actually received messages.

## What this does not restore

There is no live sender, no Telegram credentials, no private execution of the agent, no queue consumer, and no production delivery from the public workflow. Live tests and any deployment require separate secure infrastructure and owner authorization.

## Commands

`python -m unittest discover -s tests -v`

## Follow-up

Keep private and public contract versions aligned with a sanitized JSON schema or manually reviewed interface; never give public PR workflows access to secrets/private repositories. Run private Node integration tests in an isolated trusted environment.

## Synthetic outbox state-machine contract v0.3.0

`telegram_outbox_contract.py` and `tests/test_telegram_outbox_contract.py` specify six additional pure tests for `pending → claimed → delivered/failed/dead`, receipt requirements, retry limits and terminal states.

**Important:** this state machine does not provide persistence, locking, transactional deduplication, retry scheduling or exactly-once Telegram delivery. The actual trusted notification service must implement these with a private durable datastore (for example Cloudflare Durable Objects or a transactional database), and verify Telegram API responses. The public runner must never be configured as the production queue consumer.



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
