import unittest
from unittest.mock import patch, MagicMock
from bank_app.main import  main
from bank_app.account_transactions import(
    deposit,
    withdraw,
    get_account,
    tranfer_money,
    list_accounts,
)
from bank_app.create_account import (
    validate_account_type,
    check_duplicate_account,
    create_new_account,)
from bank_app.security import Security, authenticate_user
from bank_app.storage_management import ReadWrite
from bank_app.account import BankAccount


class TestMainModule(unittest.TestCase):
    def setUp(self):
        """Set up mock data for tests."""
        self.mock_accounts = {
            "Alice": {
                "Checking": BankAccount("Alice", "Checking", 500.0, Security.hash_password("password123")),
                "Savings": BankAccount("Alice", "Savings", 1000.0, Security.hash_password("password123")),
            }
        }
        self.mock_rw = ReadWrite("test_accounts.json")

    def test_validate_account_type(self):
        """Test valid and invalid account types."""
        self.assertIsNone(validate_account_type("Checking"))
        self.assertIsNone(validate_account_type("Savings"))
        with self.assertRaises(ValueError):
            validate_account_type("InvalidType")

    def test_check_duplicate_account(self):
        """Test for duplicate account detection."""
        with self.assertRaises(ValueError):
            check_duplicate_account(self.mock_accounts, "Alice", "Checking")

    def test_create_new_account(self):
        """Test account creation."""
        new_account = create_new_account("Bob", "Savings", 300.0, Security.hash_password("securepass"))
        self.assertEqual(new_account.owner, "Bob")
        self.assertEqual(new_account.account_type, "Savings")
        self.assertEqual(new_account.get_balance(), 300.0)

    def test_authenticate_user(self):
        """Test user authentication."""
        self.assertTrue(authenticate_user(self.mock_accounts, "Alice", "password123"))
        self.assertFalse(authenticate_user(self.mock_accounts, "Alice", "wrongpassword"))
        self.assertFalse(authenticate_user(self.mock_accounts, "Bob", "password123"))

    def test_deposit(self):
        """Test deposit functionality."""
        deposit(self.mock_accounts, "Alice", 200.0, "Checking")
        self.assertEqual(self.mock_accounts["Alice"]["Checking"].get_balance(), 700.0)

    def test_withdraw(self):
        """Test withdraw functionality."""
        withdraw(self.mock_accounts, "Alice", 200.0, "Savings")
        self.assertEqual(self.mock_accounts["Alice"]["Savings"].get_balance(), 790.0)

    def test_transfer_money(self):
        """Test money transfer functionality."""
        source_account = self.mock_accounts["Alice"]["Checking"]
        tranfer_money(self.mock_accounts, "Alice", "Alice", source_account, "Savings", 100.0, "Checking")
        self.assertEqual(source_account.get_balance(), 390.0)
        self.assertEqual(self.mock_accounts["Alice"]["Savings"].get_balance(), 1100.0)

    def test_list_accounts(self):
        """Test account listing."""
        with patch("builtins.print") as mock_print:
            list_accounts("Alice", self.mock_accounts)
            mock_print.assert_called()

    def test_get_account(self):
        """Test account listing"""
        with patch("builtins.print") as mock_print:
            get_account(self.mock_accounts, "Alice", "Savings")
            mock_print.assert_called()

    def test_read_write(self):
        """Test file read/write functionality."""
        # Save accounts
        self.mock_rw.save_accounts(self.mock_accounts)
        # Load accounts and verify
        loaded_accounts = self.mock_rw.load_accounts()
        self.assertIn("Alice", loaded_accounts)
        self.assertIn("Checking", loaded_accounts["Alice"])


if __name__ == "__main__":
    unittest.main()
