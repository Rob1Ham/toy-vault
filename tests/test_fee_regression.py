import unittest

from toy_vault import SpendRequest, ToyVaultLedger


class FeeRegressionTests(unittest.TestCase):
    def setUp(self):
        self.ledger = ToyVaultLedger()
        self.ledger.add_vault("demo", "alice", {"alice", "guardian"}, 1_000)

    def test_submit_rejects_spend_that_would_go_negative(self):
        request = SpendRequest("demo", "bob", 990, 20,
                               ("alice", "guardian"), "reg-fee-1")
        with self.assertRaisesRegex(ValueError, "amount and fee"):
            self.ledger.submit("alice", request)
        self.assertEqual(self.ledger.vaults["demo"]["balance"], 1_000)

    def test_submit_agrees_with_preview(self):
        request = SpendRequest("demo", "bob", 100, 10,
                               ("alice", "guardian"), "reg-fee-2")
        preview = self.ledger.preview(request)
        receipt = self.ledger.submit("alice", request)
        self.assertEqual(preview["remaining_sats"], receipt["remaining_sats"])


if __name__ == "__main__":
    unittest.main()
