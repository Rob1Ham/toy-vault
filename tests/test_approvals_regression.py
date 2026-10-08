import unittest

from toy_vault import SpendRequest, ToyVaultLedger


class ApprovalRegressionTests(unittest.TestCase):
    def setUp(self):
        self.ledger = ToyVaultLedger()
        self.ledger.add_vault("demo", "alice", {"alice", "guardian"}, 1_000)

    def test_same_name_twice_is_one_approver(self):
        request = SpendRequest("demo", "bob", 100, 10,
                               ("alice", "alice"), "reg-appr-1")
        with self.assertRaisesRegex(ValueError, "two different"):
            self.ledger.submit("alice", request)
        self.assertEqual(self.ledger.vaults["demo"]["balance"], 1_000)
        self.assertNotIn("bob", self.ledger.credits)

    def test_two_different_approvers_still_work(self):
        request = SpendRequest("demo", "bob", 100, 10,
                               ("alice", "guardian"), "reg-appr-2")
        self.ledger.submit("alice", request)
        self.assertEqual(self.ledger.credits["bob"], 100)
        self.assertEqual(self.ledger.vaults["demo"]["balance"], 890)


if __name__ == "__main__":
    unittest.main()
