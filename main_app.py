import json



from bank_app.authentication import (Security, 
                             hash_user_password, 
                             authenticate_user, 
                             validate_account_type)
from bank_app.storage_management import ReadWrite
from bank_app.reporting import  view_account_transactions
from bank_app.account_management import (create_account, 
                             create_new_account)
from bank_app.transactions import (withdraw, 
                                   deposit, 
                                   list_accounts, 
                                   get_account, 
                                   tranfer_money)


def main():
    print("Welcome to the Customer CLI")
    try: 
        accounts = ReadWrite("./data/accounts.json").load_accounts() 
        
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
            print("Invalid input. Please enter a number 1-9.")
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
                    new_account = create_new_account(owner, acc_type, initial_balance, hashed_password)
                    if owner not in accounts:
                        accounts[owner] = {}
                    accounts[owner][acc_type] = new_account
                    ReadWrite('data/accounts.json').save_accounts(accounts)

            elif choice == 2: # Add account

                password = input("Enter your password: ")
                if owner in accounts:
                    if not authenticate_user(accounts, owner, password):
                        print("Authentication failed. Try again later.")
                        continue
                    else:
                        create_account(accounts, owner, acc_type, initial_balance, password)
                        ReadWrite("data/accounts.json").save_accounts(accounts)
                else:
                    print(f"{owner} is not registered. Please create an account.")

        elif choice in [3, 4]:  # Deposit, Withdraw
            owner = input("Enter your name: ").capitalize().strip()
            acc_type = input("Select account type (Checking/Savings): ").capitalize()
            amount = float(input('Enter amount: '))
            password = input('Enter your password: ').strip()
            if not isinstance(amount, (float, int)):
                print("Amount must be a number.")
                continue
            else:
                if acc_type not in ('Checking', 'Savings'):
                    print('Please choose Checking / Savings')
                    continue
                else:
                    try:
                        if choice == 3:  # Deposit  
                            if authenticate_user(accounts, owner, password):
                                deposit(accounts, owner, amount, acc_type)                       
                                ReadWrite("data/accounts.json").save_accounts(accounts)
                            else:
                                print("Authentication failed. Try again later.")
                                continue
                                

                        elif choice == 4:  # Withdraw
                            if not authenticate_user(accounts, owner, password):
                                print("Authentication failed. Try again later.")
                                continue
                            else:
                                withdraw(accounts, owner, amount, acc_type)
                                ReadWrite("data/accounts.json").save_accounts(accounts)
                            
                    except KeyError:
                        print("Account not found. Please check the account details and try again.")
            
        elif choice == 7:  # Check Balance
            owner = input("Enter you name: ").capitalize().strip()
            acc_type = input("Enter account type: ").capitalize().strip()
            password = input("Enter your password: ")
            if acc_type not in ('Checking', 'Savings'):
                print("Please choose Savings / Checking")
            else:
                if not authenticate_user(accounts,owner, password):
                    print("Authentication failed. Try again later.")
                    continue
                else:
                    account = accounts[owner][acc_type]
                    print(f"Your {acc_type} account balance is: {account.get_balance()}")
            
        elif choice == 5:  # View Account Transactions
            owner = input("Enter your name: ").capitalize().strip()
            password = input('Enter your password: ').strip()
            view_account_transactions(accounts, owner, password)
            

        elif choice == 6:  # Transfer Money
            owner = input("Enter your name: ").capitalize().strip()
            source_acc_type = input("Select source account type (Checking/Savings): ").capitalize().strip()
            target_owner = input("Enter target account owner: ").capitalize().strip()
            target_acc_type = input("Select target account type (Checking/Savings): ").capitalize().strip()
            account = get_account(accounts, owner, source_acc_type)
            amount = float(input("Enter amount: "))
            password = input('Enter your password: ').strip()
            if not isinstance(amount, (float, int)):
                print("Amount must be an number.")
                continue
            else:
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
            print("Invalid choice. Please choose option [1-9].")
    

if __name__ == "__main__":
    main()


