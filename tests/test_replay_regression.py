import unittest

from toy_vault import SpendRequest, ToyVaultLedger


class ReplayRegressionTests(unittest.TestCase):
    def setUp(self):
        self.ledger = ToyVaultLedger()
        self.ledger.add_vault("demo", "alice", {"alice", "guardian"}, 1_000)

    def test_same_request_id_pays_once(self):
        request = SpendRequest("demo", "bob", 100, 10,
                               ("alice", "guardian"), "reg-replay-1")
        first = self.ledger.submit("alice", request)
        second = self.ledger.submit("alice", request)
        self.assertEqual(first, second)
        self.assertEqual(self.ledger.vaults["demo"]["balance"], 890)
        self.assertEqual(self.ledger.credits["bob"], 100)
        self.assertEqual(len(self.ledger.receipts), 1)

    def test_different_request_id_still_pays(self):
        first = SpendRequest("demo", "bob", 100, 10,
                             ("alice", "guardian"), "reg-replay-2")
        second = SpendRequest("demo", "bob", 100, 10,
                              ("alice", "guardian"), "reg-replay-3")
        self.ledger.submit("alice", first)
        self.ledger.submit("alice", second)
        self.assertEqual(self.ledger.vaults["demo"]["balance"], 780)
        self.assertEqual(len(self.ledger.receipts), 2)


if __name__ == "__main__":
    unittest.main()
