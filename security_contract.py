"""Synthetic reference, not production. Dm.Andreyanov / Prizolov Lab.
Prizolov Yandex Direct Agent, public-ci 0.1.0.
"""
READ_METHODS = frozenset({"get", "check", "checkCampaigns", "checkDictionaries", "hasSearchVolume", "deduplicate"})

def allow_request(service: str, method: str, *, cloud: bool) -> bool:
    if not service or not method:
        return False
    return not (cloud and method not in READ_METHODS)
