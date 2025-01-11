
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
        print("Account found")
        return accounts[owner][acc_type]
    else:
        print('Account not found.')
        return None

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


