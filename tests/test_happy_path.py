import unittest

from toy_vault import SpendRequest, ToyVaultLedger


class HappyPathTests(unittest.TestCase):
    def setUp(self):
        self.ledger = ToyVaultLedger()
        self.ledger.add_vault("demo-vault", "alice", {"alice", "guardian"}, 10_000)

    def test_preview_and_single_spend(self):
        request = SpendRequest("demo-vault", "bob", 2_000, 50,
                               ("alice", "guardian"), "demo-001")
        self.assertEqual(self.ledger.preview(request)["remaining_sats"], 7_950)
        receipt = self.ledger.submit("alice", request)
        self.assertEqual(receipt["remaining_sats"], 7_950)
        self.assertEqual(self.ledger.credits["bob"], 2_000)
        self.assertEqual(self.ledger.fees_sats, 50)

    def test_unknown_approver_is_rejected(self):
        request = SpendRequest("demo-vault", "bob", 1_000, 10,
                               ("alice", "stranger"), "demo-002")
        with self.assertRaises(ValueError):
            self.ledger.submit("alice", request)


if __name__ == "__main__":
    unittest.main()
