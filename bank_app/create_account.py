from .account import BankAccount

def validate_account_type(acc_type):
    """Validate the account type input."""
    if acc_type not in ["Checking", "Savings"]:
        raise ValueError("Invalid account type. Please choose either 'Checking' or 'Savings'.")

def check_duplicate_account(accounts, owner, acc_type):
    """Check if the user already has an account of the given type."""
    if acc_type in accounts.get(owner, {}):
        raise ValueError(f"You already have a {acc_type} account.")


def create_new_account(owner, acc_type, initial_balance, hashed_password):
    """Create a new BankAccount instance."""
    return BankAccount(owner, acc_type, initial_balance, hashed_password)

def create_account(accounts, owner, acc_type, initial_balance, password):
    """
    Create a new bank account for a user, separating concerns into smaller tasks.
    """
    try:
        # Validate account type
        if not validate_account_type(acc_type):
            # Check if account already exists
            if  not check_duplicate_account(accounts, owner, acc_type):
                account = BankAccount(owner, acc_type, initial_balance, password)
                # Save the account to the dictionary
                if owner in accounts and acc_type not in accounts[owner]:
                    accounts[owner] = {}
                accounts[owner][acc_type] = account

                print(f"Welcome {owner}, your {acc_type} account was created successfully! Balance: {initial_balance}")
                return True  # Indicate success
    except ValueError as e:
        print(f"Account creation failed: {e}")
        return False  # Indicate failure
