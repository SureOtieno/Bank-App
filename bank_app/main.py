import json
import os
import bcrypt

from bank_account import BankAccount


class Security:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


class ReadWrite:
    def __init__(self, file_name):
        self.file_name = file_name

    def save_accounts(self, accounts):
        json_data = {
            owner: {
                acc_type: {
                    "owner": acc.owner,
                    "account_type": acc.account_type,
                    "balance": acc.balance,  # Ensure balance is saved
                    "transaction_history": acc.transaction_history,
                    "password": acc.password,
                }
                for acc_type, acc in acc_types.items()
            }
            for owner, acc_types in accounts.items()
        }
        
        with open(self.file_name, 'w') as file:
            json.dump(json_data, file)
        

    def load_accounts(self):
        if not os.path.exists(self.file_name):  # Ensure the file exists
            with open(self.file_name, 'w') as file:
                json.dump({}, file)  # Create an empty dictionary structure
        else:
            try:
                with open(self.file_name, 'r') as file:
                    json_data =  json.load(file)
                accounts = {
                    owner: {
                        acc_type: BankAccount(
                            owner=data["owner"],
                            balance=data.get("balance"),
                            account_type=data["account_type"],
                            transaction_history=data.get("transaction_history", []),
                            password = data['password'],
                            
                        )
                        for acc_type, data in acc_types.items()
                    }
                    for owner, acc_types in json_data.items()}
                return accounts
            except json.JSONDecodeError:  # Handle invalid or empty JSON files
                with open(self.file_name, 'w') as file:
                    json.dump({}, file)
                return {}

def validate_account_type(acc_type):
    """Validate the account type input."""
    if acc_type not in ["Checking", "Savings"]:
        raise ValueError("Invalid account type. Please choose either 'Checking' or 'Savings'.")

def check_duplicate_account(accounts, owner, acc_type):
    """Check if the user already has an account of the given type."""
    if acc_type in accounts.get(owner, {}):
        raise ValueError(f"You already have a {acc_type} account.")

def hash_user_password(password):
    """Hash the password for secure storage."""
    return Security.hash_password(password)

def create_new_account(owner, acc_type, initial_balance, hashed_password):
    """Create a new BankAccount instance."""
    return BankAccount(owner, acc_type, initial_balance, hashed_password)

def create_account(accounts, owner, password, acc_type, initial_balance):
    """
    Create a new bank account for a user, separating concerns into smaller tasks.
    """
    try:
        # Validate account type
        validate_account_type(acc_type)

        # Check if account already exists
        check_duplicate_account(accounts, owner, acc_type)

        # Hash the password
        hashed_password = hash_user_password(password)
        password = Security.verify_password(password, hashed_password)

        # Create the new account
        account = BankAccount(accounts, owner, acc_type, initial_balance, password)

        # Save the account to the dictionary
        if owner not in accounts:
            accounts[owner] = {}
        accounts[owner][acc_type] = account

        print(f"Welcome {owner}, your {acc_type} account was created successfully! Balance: {initial_balance}")
        return True  # Indicate success
    except ValueError as e:
        print(f"Account creation failed: {e}")
        return False  # Indicate failure


def deposit(accounts, owner, amount, acc_type):
    account = accounts[owner][acc_type]
    if owner in accounts and acc_type in accounts[owner]:
        account.deposit(amount)
        print(f"Deposited {amount} into your {acc_type} account. Current Balance: {account.get_balance()}")
    else:
        print('Account not found.')

def withdraw(accounts, owner, amount, acc_type):
    account = accounts[owner][acc_type]
    if owner in accounts and acc_type in accounts[owner]:
        account.withdraw(amount)
        print(f"Withdrew {amount} from your {acc_type} account. Current Balance: {account.get_balance()}")
    else:
        print("Account not fount")

def list_accounts(owner, accounts):
    if owner not in accounts:
        print('No account found for this user')
        return 
    
    user_accounts = accounts[owner]

    if not user_accounts:
        print('You have no accounts')
    else:
        print(f'Accounts for {owner}: ')
        for acc_type, account in user_accounts.items():
            print(f'- {acc_type} Account: Balance: {account.get_balance()}')

def get_account(accounts, owner, acc_type):
    if owner in accounts and acc_type in accounts[owner]:
        return accounts[owner][acc_type]
    else:
        print('Account not found.')
        return None

def is_num():
    amount = float(input("Enter Amount: "))
    if isinstance(amount, (float, int)):
        return amount
    else:
        raise ValueError('Entry must be Integer / Float')
    
def tranfer_money(accounts, owner, target_owner, account, target_acc_type, amount, source_acc_type):
    if target_owner in accounts and target_acc_type in accounts[target_owner]:
        try:
            account.transfer(amount, accounts[target_owner][target_acc_type])
            if target_owner == owner:
                print(f"Transferred {amount} from your {source_acc_type} account to your {target_acc_type} account. New Balance: {account.get_balance()}")
            else:
                print(f"Transferred {amount} from your {source_acc_type} account to {target_owner}'s {target_acc_type} account. New Balance: {account.get_balance()}")
        except:
            print('Account do not exist.') 
    else:
        print("Source account not found. Please create the account first.")


def view_account(accounts, owner):
    if owner in accounts:
        for acc_type, account in accounts[owner].items():
            print(f"Name: {owner} Accounts: {acc_type} Account: {account}")
    else:
        print("No accounts found for this owner.")

def authenticate_user(accounts, owner, acc_type):
    if owner in accounts and acc_type in accounts[owner]:
        # Existing account found
        password = input("Enter your password: ").strip()
        hashed_password = accounts[owner][acc_type].password  # Access the password attribute
        if Security.verify_password(password, hashed_password):
            print("Authentication successful!")
        else:
            print("Incorrect password.")
            return False
        return True
        
    else:
        print(f"Account not found. Please create an account.")
        return False

  

def main():
    print("Welcome to the Customer CLI")
    try:
        accounts = ReadWrite("accounts.json").load_accounts() 
    # print(accounts) 
        
    except FileNotFoundError:
        print('No existing file found. Creating an empty one now...')
        accounts = {}
    except json.JSONDecodeError:
        print("Corrupted data file. Starting fresh.")
        accounts = {}

    
    while True:
        print("\nOptions:")
        print("1: Create New Account")
        print("2: Add Account")
        print("3: Make Deposit")
        print("4: Withdraw Money")
        print("5: View Account")
        print("6: Transfer Money")
        print("7: Account Balance")
        print("8: List Accounts")
        print("9: Exit")

        try:
            choice = int(input("Choose an Option: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice in [1, 2]:  # Account Creation
            owner = input("Please enter your name: ").capitalize()
            acc_type = input("Select account type (Checking/Savings): ").capitalize()
            initial_balance = float(input("Enter an initial balance: "))

            if choice  == 1: # Create New account
                password = input('Set a password for your account: ')
                validate_account_type(acc_type)   
                hashed_password = hash_user_password(password)
                if choice == 1:  # Create New Account
                    new_account = create_new_account(owner, acc_type, initial_balance, hashed_password)
                    if owner not in accounts:
                        accounts[owner] = {}
                    accounts[owner][acc_type] = new_account

                # We will add our data persistence code here...
                
                ReadWrite('accounts.json').save_accounts(accounts)

            elif choice == 2: # Add account
                password = input("Enter your password: ")
                authenticate_user(accounts, owner, acc_type)
                create_account(accounts, owner, password, acc_type, initial_balance)
                ReadWrite("accounts.json").save_accounts(accounts)

        elif choice in [3, 4, 7]:  # Deposit, Withdraw, or Check Balance
            owner = input("Please enter your name: ").capitalize()
            acc_type = input("Select account type (Checking/Savings): ").capitalize()
            amount = float(input('Enter amount: '))
            # password = input('Enter your password: ')
            # hashed_password = Security.hash_password(password)
            
            try:
                if choice == 3:  # Deposit
                    # print(account)
                    if not isinstance(amount, (float, int)):
                        raise TypeError("Amount must be a number.")

                    if authenticate_user(accounts, owner, acc_type):
                        deposit(accounts, owner, amount, acc_type)
                        
                        ReadWrite("accounts.json").save_accounts(accounts)
                elif choice == 4:  # Withdraw
                    if not isinstance(amount, (float, int)):
                        raise TypeError("Amount must be a number.")
                    # amount = is_num()
                    withdraw(accounts, owner, amount, acc_type)
                    
                    ReadWrite("accounts.json").save_accounts(accounts)
                    
                elif choice == 7:  # Check Balance
                    print(f"Your {acc_type} account balance is: {account.get_balance()}")
            except KeyError:
                print("Account not found. Please check the account details and try again.")
            
            
        elif choice == 5:  # View Account
            owner = input("Please enter your name: ").capitalize()
            view_account(accounts, owner)
            

        elif choice == 6:  # Transfer Money
            owner = input("Enter your name: ").capitalize().strip()
            source_acc_type = input("Select source account type (Checking/Savings): ").capitalize().strip()
            target_owner = input("Enter target account owner: ").capitalize().strip()
            target_acc_type = input("Select target account type (Checking/Savings): ").capitalize().strip()
            account = get_account(accounts, owner, source_acc_type)
            amount = is_num()
            tranfer_money(accounts, owner, target_owner, account, target_acc_type, amount, source_acc_type)
            
            ReadWrite("accounts.json").save_accounts(accounts)

        elif choice == 8: # List Accounts
            owner = input('Enter your name: ').capitalize()

            list_accounts(owner, accounts)
        
        elif choice == 9:  # Exit
            confirm_exit = input("Are you sure you want to exit? (yes/no): ").lower()
            if confirm_exit == "yes":
                print("Exiting... Thank you for using the Customer CLI!")
                break
            else:
                print("Returning to the main menu.")
        else:
            print("Invalid choice. Please choose a valid option.")
    

if __name__ == "__main__":
    main()


