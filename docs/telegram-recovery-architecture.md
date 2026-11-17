# Telegram restoration architecture — public runner feasibility

Author: **Dm.Andreyanov** · Brand: **Prizolov Lab** · Product: **Prizolov Yandex Direct Agent** · Version: **recovery-design 0.1.0**

## Confirmed diagnosis (17 November 2026)

- Private `direct-agent` and `direct-agent-data` Actions jobs fail **before any step or runner assignment**. The private project issue [#2](https://github.com/prizolov-lab/direct-agent/issues/2) records GitHub's annotation: *"The job was not started because recent account payments have failed or your spending limit needs to be increased."*
- The public synthetic workflow [run 43932909073](https://github.com/prizolov-lab/direct-agent-ci-public/actions/runs/43932909073) passed on Python 3.10 and 3.12. This proves **only** that the public repository can run synthetic workflows.
- Public repo does not contain or execute the private bot, data, client configuration, queue, or secrets. Successful synthetic CI is **not** proof of Telegram recovery.

## Immediate safe steps (no production effects)

1. Keep `direct-agent-ci-public` as a synthetic CI harness unless a separate, explicitly reviewed public-safe relay is approved.
2. Fix the GitHub billing/spending hold on `prizolov-lab`, then restart **one** Telegram job in the private data repo with a read-only dry-run gate first.
3. Record `sendMessage` response IDs, API error codes and retry attempts in private state; treat `offered.json` as an attempted offer, not delivery proof.
4. Before queue replay, quarantine/inspect stale callbacks: do **not** auto-execute aged undo, stop, budget, deletion or launch requests. Match client, signed request hash, expiry, current cabinet snapshot and owner identity.
5. Resume read-only status commands first, then ordinary owner notifications, then explicitly approved fresh operation requests; validate daily, intraday and mail separately.

## Optional alternate architecture — requires additional design/security review

```
Private bot runtime (owned server or trusted worker)
  ├── authenticates Telegram webhook by secret
  ├── stores queue/offset + delivery receipts in private database
  ├── sends ordinary notifications via Bot API using secrets kept server-side
  ├── validates owner-only callbacks + signatures + expirations
  └── dispatches restricted cabinet operations only with fresh approvals

Public repository:
  └── synthetic contract tests; NO bot token, private repo token, client data,
      callback payloads, full queue, approval signatures or production dispatch
```

Do **not** publish a workflow that clones the private agent with an elevated token into public Actions merely to evade the billing restriction. Such a workflow increases the risk of proprietary code or credentials leaking through logs, artifacts, runner access or pull request contexts. Public Actions limits are also governed by GitHub policies and may be affected by account-level restrictions.

## Acceptance conditions

- A Telegram notification actually reaches the configured owner chat, with non-sensitive test content and a correlated `message_id`.
- Incoming `/board` produces exactly one response and does not mutate any advertising account.
- Failed delivery is visible and retryable with stable deduplication.
- Stale approval buttons are **not** resent or executed automatically.
- Private production code passes its own tests and review, independently of public synthetic CI.
- No approval, advertising budget, campaign state, or billing setting changes without owner authorization.

## Related work

- [Private Approval Recovery draft PR #3](https://github.com/prizolov-lab/direct-agent/pull/3)
- [Private data-repository P0 incident #1](https://github.com/prizolov-lab/direct-agent-data/issues/1)

This document is operational guidance and a technical design **only**: publishing it does not deploy, send Telegram messages, bypass billing restrictions, or restore the agent.
