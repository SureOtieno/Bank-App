import json, os

from .account import BankAccount

class ReadWrite:
    def __init__(self, file_name):
        self.file_name = file_name

    def save_accounts(self, accounts):
        json_data = {
            owner: {
                acc_type: {
                    **acc.__dict__,
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
                            account_type=data["account_type"],
                            password = data['password'],
                            balance=float(data.get("_BankAccount__balance")),
                            transaction_history=data.get("transaction_history", []),
                            
                        )
                        for acc_type, data in acc_types.items()
                    }
                    for owner, acc_types in json_data.items()}
                return accounts
            except json.JSONDecodeError:  # Handle invalid or empty JSON files
                with open(self.file_name, 'w') as file:
                    json.dump({}, file)
                return {}
