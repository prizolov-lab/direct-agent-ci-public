# Prizolov Yandex Direct Agent — execution migration v1.0.0

Author: **Dm.Andreyanov** · Brand: **Prizolov Lab**

## Verified
- Private `direct-agent-data` workflow run 44160601303: job failed with zero steps, GitHub billing budget Actions $0/$0 blocked.
- Public `direct-agent-ci-public` workflow run 44172258302: `public-runner-readiness` succeeded.
- This repo has only public, non-executable status validation and synthetic CI. **No Yandex API operations were migrated.**

## Boundary
- Public Actions may run tests and report fixed non-sensitive statuses only.
- Never checkout private `direct-agent` or `direct-agent-data` on public GitHub-hosted runners.
- Never provision Yandex tokens, private repo tokens, CRM secrets, owner approvals, customer names, command text, campaign IDs, budget values or private reports here.
- Public event schema is intentionally limited to `schema=1` and `event in {runner_ready, execution_blocked, review_required}`. No command or user-controlled message content.
- Public CI is **not** an executor, not a broker for campaign changes, and not a source of approval.

## Required secure executor (not deployed)
- Private host or protected runner controlled by the owner, not public Actions.
- Credentials stored in a managed secret store, least privilege per client, no secrets in code/logs.
- Signed authenticated requests with expiry, nonce/replay protection, client scoping and allowlisted operations.
- Read-only Direct/Metrica health check first. Confirm account identity before any write.
- Material campaign, budget, strategy, publication or analytics changes require owner approval bound to exact action and parameters; independent QA and before/after state verification.
- Persist immutable audit log and error state; do not retry uncertain writes blindly.
- Test isolation, failure handling, approval enforcement and secret exposure before connecting real clients.

## Next activation options
1. Unblock private GitHub Actions billing and run existing `run.yml` read-only.
2. Deploy a protected executor on an existing private server or equivalent infrastructure; retain public CI for tests only.

Neither option has been executed in this change. No campaign changes are authorized.
