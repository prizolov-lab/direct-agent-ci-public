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
