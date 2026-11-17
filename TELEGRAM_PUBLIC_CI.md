# Existing Telegram bot through public Actions, v1.0.0

Author: **Dm.Andreyanov** · Brand: **Prizolov Lab** · Product: **Prizolov Yandex Direct Agent**

## Actual execution path

Chat with GitHub connector → add a new public fixed-event marker on main →
`telegram-owner.yml` on a public GitHub runner → existing Telegram bot → configured owner.

This removes the dependency on dispatching `run.yml` in private `direct-agent-data`.
It does not require a new bot, Cloudflare login, Worker deployment, KV or webhook changes.

## One-time credentials

In this repository's Settings → Secrets and variables → Actions, configure:
- `TELEGRAM_BOT_TOKEN`: token of the existing Prizolov bot.
- `TELEGRAM_OWNER_CHAT_ID`: numeric ID of the already connected owner's chat.

Use the existing trusted values. Do not create a new bot, post values in chat, commit them, print them,
or copy private source/customer files here. Adding or transferring credentials requires the owner's approval.
The GitHub file connector cannot read or provision Actions secrets. Secret setup is a separate secure operation.

## Send from a connected chat

Create one new file in main with a stable unique event ID, for example
`notifications/owner/owner_probe_20261117_001.json`:

```json
{"event":"test"}
```

Allowed events: `test`, `started`, `completed`, `blocked`, `review`.
Each generates a fixed Russian service notice for the executor Doctor PUH with Moscow timestamp.
Only the configured owner's chat is accepted. No arbitrary recipient, message text, report contents or
client names are accepted. Do not put private text into a marker, workflow input, commit message or public log.

Use a new marker only for a genuinely new notification. Do not modify a prior marker.
A push containing multiple markers is refused. Renamed/modified/deleted markers are refused.
There is no historical backlog consumer; old markers are not scanned or replayed.

Alternatively, run the workflow manually on main with a fixed `event` choice:

```powershell
gh workflow run telegram-owner.yml --repo prizolov-lab/direct-agent-ci-public --ref main -f event=test
```

## Verify the result

Find the public workflow run for that exact commit and inspect the sender step.
Only `{"status":"delivered","message_id":123}` proves Telegram accepted the message.
It does not prove the human read it.
Missing credentials report `blocked_missing_or_invalid_...`; no network send occurs.
A Telegram rejection reports `telegram_rejected`.
Transport uncertainty or an invalid receipt reports `unknown_no_automatic_retry`.

Do not retry a run or create a new marker after an unknown response before checking Telegram.
Rerun attempts are intentionally disabled. A fresh manual run/commit is not global exactly-once delivery:
an authorized user can deliberately issue a new event. Concurrency serializes notices but does not
provide a cross-run durable outbox. This workflow is not a consumer for private client reports/approvals.

## Trust boundary

Only main in `prizolov-lab/direct-agent-ci-public`, actor `prizolov-lab`, and the first run attempt are allowed.
Forks, PRs, other actors/branches/events and free-form payloads cannot send.
The live sender has read-only GitHub permissions and no persisted checkout credentials.
Synthetic PR/push tests do not receive Telegram secrets. Only the live sending step receives the two named secrets.
No raw transport exception or Telegram response body is logged.

## Delivery status

The implementation is connected at code level only after main is updated.
Credentials and an actual accepted Telegram response must be verified separately; never declare delivery from green synthetic tests.
