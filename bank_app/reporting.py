from .authentication import authenticate_user

def view_account_transactions(accounts, owner, password):
    if authenticate_user(accounts,owner, password):
        user_account = accounts.get(owner)
        if user_account:
            print(f"Name: {owner}")
            for acc_type, account in user_account.items():
                print(f"Account: {acc_type}") 
                for transaction in account.get_transaction_history():
                    print(f"Transactions: {transaction}")
        else:
            print("No accounts found for this owner.")
    else:
        print("Authentication failed. Try again later.")
