import unittest
import json, os

from bank_app.account import BankAccount

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """Setup runs before each test."""
        self.account = BankAccount(owner='Test User', account_type='Checking', balance=1000, password='abcd1234')

    def tearDown(self):
        """Tear down runs after each test."""
        del self.account

    def test_initialization(self):
        self.assertEqual(self.account.owner, "Test User")
        self.assertEqual(self.account.get_balance(), 1000)
        self.assertEqual(self.account.account_type, "Checking")

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.get_balance(), 1500)

    def test_withdraw(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.get_balance(), 790)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(2000)

    def test_transfer(self):
        target_account = BankAccount(owner='Target user', account_type='Savings', balance=500, password='abcd1234')
        self.account.transfer(300, target_account)
        self.assertEqual(self.account.get_balance(), 690)
        self.assertEqual(target_account.get_balance(), 800)

    def test_sserialization(self):
        data = self.account.to_dict()
        self.assertEqual(data['owner'], 'Test User')
        self.assertEqual(data['balance'], 1000)

    def test_save_and_load(self):
        # Save to file
        filename = "test_account.json"
        with open(filename, "w") as f:
            json.dump(self.account.to_dict(), f)

        # Load from file
        with open(filename, "r") as f:
            data = json.load(f)
        
        loaded_account = BankAccount.from_dict(data)
        self.assertEqual(loaded_account.owner, self.account.owner)
        self.assertEqual(loaded_account.get_balance(), self.account.get_balance())
        self.assertEqual(loaded_account.account_type, self.account.account_type)

        # Clean up
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
