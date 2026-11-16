# Public CI versus private release gates

Author: **Dm.Andreyanov** · Brand: **Prizolov Lab**  
Product: **Prizolov Yandex Direct Agent** · Version: **public-ci 0.1.1**

## Verified scope
The public workflow runs standalone synthetic guard tests on Python 3.10 and 3.12.
It does **not** checkout, import, build, or execute private `direct-agent` code.

## Mandatory private release checks
1. Run the **actual private** unit suite on Python 3.10 and 3.12.
2. Run the Windows lock contention test on Windows.
3. Run the linter and dependency validation against the private source.
4. Verify transport-level cloud mutation denial for Direct and Metrika with network calls mocked.
5. Verify approved local writes, forged environment flags, error handling, and budget bounds.
6. Review all changes in draft PR #1 and record test evidence.
7. Only after passing checks, obtain explicit authorization for merging or any live account operation.

## Prohibited shortcuts
- Do not report a passing public workflow as passing private CI.
- Do not put `direct-agent-data`, customer files, secrets, or private code into this repository.
- Do not give this public workflow a token with access to private repositories.
- Do not bypass cloud write restrictions to make a test pass.

## Current blocker
Private GitHub Actions jobs were refused **before starting** because of account
billing/spending restrictions; see private repository issue #2.
Public synthetic tests are not a substitute for resolving that gate.

## Offline option
The private test suite can also be run on a trusted local machine with both Python
versions and Windows available. Keep logs free of tokens and customer data.
