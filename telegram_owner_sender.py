# Author — Dm.Andreyanov | Brand — Prizolov Lab
# Product — Prizolov Yandex Direct Agent | public-owner-notify v1.0.0
"""Send only fixed owner service notifications. Never accepts client data or arbitrary chat IDs."""
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import re
import sys
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

REPO = "prizolov-lab/direct-agent-ci-public"
ACTOR = "prizolov-lab"
MESSAGES = {
    "test": "Проверка доставки уведомлений владельцу.",
    "started": "Работа исполнителя начата.",
    "completed": "Работа исполнителя завершена. Подробности доступны в приватном проекте.",
    "blocked": "Работа исполнителя заблокирована. Требуется проверка приватного проекта.",
    "review": "Результат подготовлен к независимой проверке в приватном проекте.",
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def preflight(env):
    expected = {"GITHUB_REPOSITORY": REPO, "GITHUB_REF": "refs/heads/main",
                "GITHUB_ACTOR": ACTOR, "GITHUB_RUN_ATTEMPT": "1"}
    if (env.get("GITHUB_EVENT_NAME") not in ("workflow_dispatch", "push") or
            any(env.get(k) != v for k, v in expected.items())):
        return "blocked_untrusted_context"
    if env.get("NOTICE_EVENT", "test") not in MESSAGES:
        return "blocked_unknown_event"
    token = env.get("TELEGRAM_BOT_TOKEN", "")
    chat = env.get("TELEGRAM_OWNER_CHAT_ID", "")
    if not re.fullmatch(r"[0-9]+:[A-Za-z0-9_-]{20,}", token):
        return "blocked_missing_or_invalid_bot_token"
    if not re.fullmatch(r"-?[1-9][0-9]*", chat):
        return "blocked_missing_or_invalid_owner_chat"
    return None


def send(env, opener=None, now=None):
    error = preflight(env)
    if error:
        return {"status": error}
    when = (now or dt.datetime.now(ZoneInfo("Europe/Moscow"))).strftime("%d.%m.%Y %H:%M МСК")
    text = ("Prizolov Lab — служебное уведомление.\nИсполнитель: Доктор ПУХ.\n" +
            when + "\n" + MESSAGES[env.get("NOTICE_EVENT", "test")])
    body = {"chat_id": env["TELEGRAM_OWNER_CHAT_ID"], "text": text, "disable_web_page_preview": True}
    request = urllib.request.Request("https://api.telegram.org/bot" + env["TELEGRAM_BOT_TOKEN"] + "/sendMessage",
                                     data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
    try:
        with (opener or urllib.request.build_opener(NoRedirect())).open(request, timeout=30) as response:
            payload = json.loads(response.read(65537))
    except urllib.error.HTTPError as exc:
        # No exception text, request URL, response description or private content enters logs.
        try:
            payload = json.loads(exc.read(65537))
        except (ValueError, OSError):
            return {"status": "unknown_no_automatic_retry"}
        if isinstance(payload, dict) and payload.get("ok") is False:
            return {"status": "telegram_rejected"}
        return {"status": "unknown_no_automatic_retry"}
    except (OSError, ValueError):
        return {"status": "unknown_no_automatic_retry"}
    if not isinstance(payload, dict):
        return {"status": "unknown_no_automatic_retry"}
    if payload.get("ok") is False:
        return {"status": "telegram_rejected"}
    result = payload.get("result")
    if not isinstance(result, dict):
        return {"status": "unknown_no_automatic_retry"}
    mid, chat = result.get("message_id"), result.get("chat")
    if (payload.get("ok") is not True or type(mid) is not int or mid <= 0 or not isinstance(chat, dict) or
            str(chat.get("id")) != env["TELEGRAM_OWNER_CHAT_ID"]):
        return {"status": "unknown_no_automatic_retry"}
    return {"status": "delivered", "message_id": mid}


def push_event(env):
    """Public marker contains only one fixed event; private text never enters Actions inputs."""
    before, after = env.get("NOTICE_BEFORE", ""), env.get("GITHUB_SHA", "")
    if any(not re.fullmatch(r"[0-9a-f]{40}", sha) or sha == "0" * 40 for sha in (before, after)):
        raise ValueError("invalid_commit")
    diff = subprocess.run(["git", "diff", "--name-status", before, after, "--", "notifications/owner/"],
                          check=True, capture_output=True, text=True, timeout=15)
    rows = [line.split("\t") for line in diff.stdout.splitlines() if line]
    if len(rows) != 1 or len(rows[0]) != 2 or rows[0][0] != "A":
        raise ValueError("exactly_one_new_marker_required")
    path = rows[0][1]
    if not re.fullmatch(r"notifications/owner/[A-Za-z0-9_-]{8,100}\.json", path):
        raise ValueError("invalid_marker_path")
    file = Path(path)
    if file.is_symlink() or file.stat().st_size > 256:
        raise ValueError("invalid_marker_file")
    payload = json.loads(file.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"event"} or payload["event"] not in MESSAGES:
        raise ValueError("only_fixed_event_allowed")
    return payload["event"]


def main():
    try:
        env = dict(os.environ)
        if env.get("GITHUB_EVENT_NAME") == "push":
            env["NOTICE_EVENT"] = push_event(env)
        result = send(env)
    except Exception:
        # Fail closed without printing stack traces that may include credential URLs.
        result = {"status": "unknown_no_automatic_retry"}
    print(json.dumps(result))
    return 0 if result["status"] == "delivered" else 1


if __name__ == "__main__":
    sys.exit(main())
