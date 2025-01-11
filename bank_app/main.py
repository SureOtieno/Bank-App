import json

from .security import (Security, hash_user_password, authenticate_user)
from .storage_management import ReadWrite
from .create_account import (create_account, 
                             create_new_account, 
                             validate_account_type)
from .account_transactions import (withdraw, 
                                   deposit, 
                                   list_accounts, 
                                   view_account_transactions, 
                                   get_account, 
                                   tranfer_money)


def main():
    print("Welcome to the Customer CLI")
    try: 
        accounts = ReadWrite("data/accounts.json").load_accounts() 
        
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
        print("5: View Account Transactions")
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
            owner = input("Enter your name: ").capitalize().strip()
            acc_type = input("Select account type (Checking/Savings): ").capitalize().strip()
            initial_balance = float(input("Enter an initial balance: "))

            if choice  == 1: # Create New account
                password = input('Set a password for your account: ')
                validate_account_type(acc_type)   
                hashed_password = hash_user_password(password)
                if choice == 1:  # Create New Account
                    new_account = create_new_account(owner, acc_type, hashed_password, initial_balance)
                    if owner not in accounts:
                        accounts[owner] = {}
                    accounts[owner][acc_type] = new_account

                ReadWrite('data/accounts.json').save_accounts(accounts)

            elif choice == 2: # Add account
                password = input("Enter your password: ")
                if authenticate_user(accounts, owner, password):
                    create_account(accounts, owner, password, acc_type, initial_balance)
                    ReadWrite("data/accounts.json").save_accounts(accounts)

        elif choice in [3, 4, 7]:  # Deposit, Withdraw, or Check Balance
            owner = input("Enter your name: ").capitalize().strip()
            acc_type = input("Select account type (Checking/Savings): ").capitalize()
            password = input('Enter your password: ').strip()
            try:
                if choice == 3:  # Deposit
                    amount = float(input('Enter amount: '))
                    if not isinstance(amount, (float, int)):
                        raise TypeError("Amount must be a number.")

                    if authenticate_user(accounts, owner, password):
                        deposit(accounts, owner, amount, acc_type)                       
                        ReadWrite("data/accounts.json").save_accounts(accounts)

                elif choice == 4:  # Withdraw
                    amount = float(input('Enter amount: '))
                    if not isinstance(amount, (float, int)):
                        raise TypeError("Amount must be a number.")
                    
                    if authenticate_user(accounts, owner, password):
                        withdraw(accounts, owner, amount, acc_type)
                    
                        ReadWrite("data/accounts.json").save_accounts(accounts)
                    
                elif choice == 7:  # Check Balance
                    account = accounts[owner][acc_type]
                    print(f"Your {acc_type} account balance is: {account.get_balance()}")
            except KeyError:
                print("Account not found. Please check the account details and try again.")
            
            
        elif choice == 5:  # View Account Transactions
            owner = input("Enter your name: ").capitalize().strip()
            password = input('Enter your password: ').strip()
            
            if authenticate_user(accounts, owner, password):
                view_account_transactions(accounts, owner)
            

        elif choice == 6:  # Transfer Money
            owner = input("Enter your name: ").capitalize().strip()
            source_acc_type = input("Select source account type (Checking/Savings): ").capitalize().strip()
            target_owner = input("Enter target account owner: ").capitalize().strip()
            target_acc_type = input("Select target account type (Checking/Savings): ").capitalize().strip()
            account = get_account(accounts, owner, source_acc_type)
            amount = float(input("Enter amount: "))
            password = input('Enter your password: ').strip()
            if not isinstance(amount, (float, int)):
                raise ValueError("Amount must be an integer")
            
            if authenticate_user(accounts, owner, password):
                tranfer_money(accounts, owner, target_owner, account, target_acc_type, amount, source_acc_type)
            
            ReadWrite("data/accounts.json").save_accounts(accounts)

        elif choice == 8: # List Accounts
            owner = input("Enter your name: ").capitalize().strip()
            password = input('Enter your password: ').strip()
            if authenticate_user(accounts,owner, password):
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


