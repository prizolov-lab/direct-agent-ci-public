"""Synthetic tests. Dm.Andreyanov / Prizolov Lab.
Prizolov Yandex Direct Agent, public-ci 0.1.0.
"""
import unittest
from security_contract import allow_request

class GuardContractTests(unittest.TestCase):
    def test_cloud_read(self):
        self.assertTrue(allow_request("campaigns", "get", cloud=True))
    def test_cloud_direct_mutation_denied(self):
        self.assertFalse(allow_request("campaigns", "update", cloud=True))
    def test_cloud_metrika_mutation_denied(self):
        self.assertFalse(allow_request("metrika", "createGoal", cloud=True))
    def test_missing_method_denied(self):
        self.assertFalse(allow_request("campaigns", "", cloud=True))
    def test_local_reference_does_not_model_authorization(self):
        self.assertTrue(allow_request("campaigns", "update", cloud=False))
