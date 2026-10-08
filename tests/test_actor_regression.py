import unittest

from toy_vault import SpendRequest, ToyVaultLedger


class ActorRegressionTests(unittest.TestCase):
    def setUp(self):
        self.ledger = ToyVaultLedger()
        self.ledger.add_vault("demo", "alice", {"alice", "guardian"}, 1_000)

    def test_stranger_cannot_submit_even_with_valid_approvals(self):
        request = SpendRequest("demo", "mallory", 100, 10,
                               ("alice", "guardian"), "reg-actor-1")
        with self.assertRaisesRegex(ValueError, "owner or an approved signer"):
            self.ledger.submit("mallory", request)
        self.assertEqual(self.ledger.vaults["demo"]["balance"], 1_000)
        self.assertNotIn("mallory", self.ledger.credits)

    def test_approved_signer_who_is_not_owner_can_submit(self):
        request = SpendRequest("demo", "bob", 100, 10,
                               ("alice", "guardian"), "reg-actor-2")
        receipt = self.ledger.submit("guardian", request)
        self.assertEqual(self.ledger.vaults["demo"]["balance"], 890)
        self.assertEqual(receipt["actor"], "guardian")


if __name__ == "__main__":
    unittest.main()
