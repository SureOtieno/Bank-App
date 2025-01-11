def view_account_transactions(accounts, owner):
    for owner, acc_types in accounts.items():
        print(f"Name: {owner} ")
        for acc_type, account in acc_types.items():
            if owner == owner:
                print(f"Account: {acc_type}") 
                print(f"Transactions: {account.get_transaction_history()}")
            else:
                print("No accounts found for this owner.")
