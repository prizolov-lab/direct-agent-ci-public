# Prizolov Yandex Direct Agent — public CI and owner notifications

Author: **Dm.Andreyanov** · Brand: **Prizolov Lab** · Product: **Prizolov Yandex Direct Agent** · Version: **public-owner-notify 1.0.0**

## What works here

- `public-ci.yml`: dependency-free synthetic security tests on Python 3.10 and 3.12, without secrets.
- `telegram-owner.yml`: real fixed service notifications to the existing owner's Telegram bot.
  Runs manually or when the trusted owner adds one new `notifications/owner/<event-id>.json` to main.
- No private repository checkout, client data, free-form notification text, Yandex API calls or Worker deployment.

For setup and operation, see [TELEGRAM_PUBLIC_CI.md](TELEGRAM_PUBLIC_CI.md).

The live workflow requires the existing bot token and owner chat ID as Actions secrets.
Missing credentials produce an explicit blocked result. Code availability and passing tests alone do not prove live delivery.
A successful send requires `delivered` and Telegram `message_id`.

Tests: `python -m unittest discover -s tests -v`.
Public synthetic checks do not validate or release private `direct-agent` code; private release gates remain separate.
