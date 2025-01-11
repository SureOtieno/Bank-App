from datetime import datetime


time = datetime.now()

class BankAccount:
    def __init__(self, owner, account_type, balance, password, transaction_history=None):
        if account_type.capitalize().strip() not in  ("Checking", "Savings"):
            raise ValueError("Account_type must either be Checking or Savings account")
        self.account_type = account_type
        self.__transaction_history = transaction_history or []
        self.owner = owner
        if balance < 0:
            raise ValueError("Balance cannot be a negative number")
        if not isinstance(balance, (int, float)):
            raise ValueError("Balance must be a number.")
        self.__balance = balance  # Private attribute
        self.password = password

    def to_dict(self):
        '''This function serializes the BankAccount object. 
        Converts the instance of BankAccount into a dictionary'''
        return {
            'owner': self.owner,
            'balance': self.get_balance(),
            'account_type': self.account_type,
            'transaction_history': self.get_transaction_history(),
            'password': self.password
        }
    
    @classmethod
    def from_dict(cls, data):
        """Creates a BankAccount instance from a dictionary."""
        return cls(
            owner=data['owner'],
            account_type=data['account_type'],
            balance=data['balance'],
            password=data['password'],
            transaction_history=data.get('transaction_history', []),            
        )



    def deposit(self, amount):
        try:
            if amount <= 0:
                raise ValueError("Deposits must be more than zero")
            if not isinstance(amount, (int, float)):
                raise ValueError("Amount must be a positive number.")
            
            self.__balance += amount
            self.__transaction_history.append(f"{time} -- Deposit: {amount}. Current Balance: {self.__balance}")
        except TypeError:
            print('Deposit must be a number')

    def withdraw(self, amount):
        if self.__balance <= amount:
            raise ValueError("Insufficient funds to make withdrawal.")

        if  amount <= 0:
            raise ValueError("Withdrawals must more than zero.")
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number.")
        
        if self.account_type == "Savings":
            if self.__balance - amount < 100:
                print("Please withdraw a lower amount")
            else:
                try:
                    if amount <= 100:
                        charge = 5
                        total_deduction = amount + charge
                        self.__balance -= total_deduction 
                        print(f"Savings Withdrawal: {amount} -- Charge: {charge}")
                        self.__transaction_history.append(f"{time} -- Savings Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
                    elif amount >100 and amount < 1000:
                        charge = 10
                        total_deduction = amount + charge
                        self.__balance -= total_deduction 
                        print(f"Savings Withdrawal: {amount} -- Charge: {charge}")
                        self.__transaction_history.append(f"{time} -- Savings Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
                    elif amount > 1000 and amount <= 5000:
                        charge = 45
                        total_deduction = amount + charge
                        self.__balance -= total_deduction 
                        print(f"Savings Withdrawal: {amount} -- Charge: {charge}")
                        self.__transaction_history.append(f"{time} -- Savings Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
                    elif amount >5000 and amount <= 10000:
                        charge = 100
                        total_deduction = amount + charge
                        self.__balance -= total_deduction 
                        print(f"Savings Withdrawal: {amount} -- Charge: {charge}")
                        self.__transaction_history.append(f"{time} -- Savings Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
                    elif amount > 10000 and amount <= 100000:
                        charge = 250
                        total_deduction = amount + charge
                        self.__balance -= total_deduction 
                        print(f"Savings Withdrawal: {amount} -- Charge: {charge}")
                        self.__transaction_history.append(f"{time} -- Savings Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
                    elif amount >100000 and amount <= 300000:
                        charge = 500
                        total_deduction = amount + charge
                        self.__balance -= total_deduction 
                        print(f"Savings Withdrawal: {amount} -- Charge: {charge}")
                        self.__transaction_history.append(f"{time} -- Savings Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
                    else:
                        print("Amount too high. Please visit your branch for assistance")

                except ValueError as e:
                    print(f"{e} Amount must be a number.")
        else:
            if amount <= 100:
                charge = 5
                total_deduction = amount + charge
                self.__balance -= total_deduction 
                print(f"Checking Withdrawal: {amount} -- Charge: {charge}")
                self.__transaction_history.append(f"{time} -- Checking Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
            elif amount >100 and amount < 1000:
                charge = 10
                total_deduction = amount + charge
                self.__balance -= total_deduction
                print(f"Checking Withdrawal: {amount}") 
                self.__transaction_history.append(f"{time} -- Checking Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
            elif amount > 1000 and amount <= 5000:
                charge = 45
                total_deduction = amount + charge
                self.__balance -= total_deduction
                print(f"Checking Withdrawal: {amount}") 
                self.__transaction_history.append(f"{time} -- Checking Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
            elif amount >5000 and amount <= 10000:
                charge = 100
                total_deduction = amount + charge
                self.__balance -= total_deduction
                print(f"Checking Withdrawal: {amount}") 
                self.__transaction_history.append(f"{time} -- Checking Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
            elif amount > 10000 and amount <= 100000:
                charge = 250
                total_deduction = amount + charge
                self.__balance -= total_deduction 
                print(f"Checking Withdrawal: {amount}")
                self.__transaction_history.append(f"{time} -- Checking Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
            elif amount >100000 and amount <= 300000:
                charge = 500
                total_deduction = amount + charge
                self.__balance -= total_deduction 
                print(f"Checking Withdrawal: {amount}")
                self.__transaction_history.append(f"{time} -- Checking Withdrawal: {amount} - charge {charge}. New Savings balance: {self.__balance}")
            else:
                print("Amount too high. Please visit your branch for assistance")
                       
            
    def transfer(self, amount, target_account):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number.")
        
        if amount >= self.__balance:
            return "The amount is too high. Choose a lower amount."
        
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        
        
        try:
            # Make dections from sender
            if amount <= 1000:
                charge = 10
                total_deductions = amount + charge
                self.__balance -= total_deductions
                self.__transaction_history.append(f"{time} -- Transfered {amount} to {self.account_type} Charge: {charge}. New balance: {self.__balance}")

            elif amount > 1000 and amount <= 10000:
                charge = 50
                total_deductions = amount + charge
                self.__balance -= total_deductions
                self.__transaction_history.append(f"{time} -- Transfered {amount} to {self.account_type} Charge: {charge}. New balance: {self.__balance}")

            elif amount >10000 and amount <= 100000:
                charge = 100
                total_deductions = amount + charge
                self.__balance -= total_deductions
                self.__transaction_history.append(f"{time} -- Transfered {amount} to {self.account_type} Charge: {charge}. New balance: {self.__balance}")

            elif amount > 100000 and amount <= 1000000:
                charge = 300
                total_deductions = amount + charge
                self.__balance -= total_deductions
                self.__transaction_history.append(f"{time} -- Transfered {amount} to {self.account_type} Charge: {charge}. New balance: {self.__balance}")

            elif amount > 1000000 and amount <= 5000000:
                charge = 1000
                total_deductions = amount + charge
                self.__balance -= total_deductions
                self.__transaction_history.append(f"{time} -- Transfered {amount} to {self.account_type} Charge: {charge}. New balance: {self.__balance}")

            else:
                print("Amount too high. Please visit your branch for assistance")
            
            # make deposit to the target account/receiver
            target_account.deposit(amount)
            target_account.__transaction_history.append(f"{time} -- Revieved {amount} from {self.owner} New balance: {target_account.__balance}")
            # else: print("Account does not exist")
        except ValueError:
            print("Target Account is not an instance of BankAccount class.")


        return f'Successfully transfered {amount} from {target_account.owner}.'
    
    def interest_calculations(self, amount, interest, period):
        pass

    def get_balance(self):
        return self.__balance
    
    def get_transaction_history(self):
        return self.__transaction_history


    def __str__(self):
        return f'{time} -- Hello {self.owner}, your account balance is {self.__balance}.'
    