class BankAccount:
    def __init__(self, owner, account_type, password, balance=0, transaction_history = []):
        if account_type.capitalize() not in  ("Checking", "Savings"):
            raise ValueError("Account_type must either be Checking or Savings account")
        self.account_type = account_type
        self.transaction_history = transaction_history
        self.owner = owner
        if not isinstance(balance, (int, float)) or balance < 0:
            raise ValueError("Balance must be a non-negative number.")
        self.__balance = balance  # Private attribute
        self.password = password

    def to_dict(self):
        '''This function serializes the BankAccount object. 
        Converts the instance of BankAccount into a dictionary'''
        return {
            'owner': self.owner,
            'balance': self.get_balance(),
            'account_type': self.account_type,
            'transaction_history': self.transaction_history,
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
            self.transaction_history.append("Deposit: {}. Current Balance: {}".format(amount, self.__balance))
        except TypeError:
            print('Deposit must be a number')

    def withdraw(self, amount):
        if self.__balance < amount:
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
                    self.__balance -= amount
                    self.transaction_history.append("Savings Withdrawal: {}. New Savings balance: {}".format(amount, self.__balance))
                except:
                    print("Withdraw failed. Please try a different amount.")
        else:
            self.__balance -= amount
            print("Checking Withdrawal: {}".format(amount))
            self.transaction_history.append("Checking Withdrawal: {}. New Checking balance: {}".format(amount, self.__balance))

    def transfer(self, amount, target_account):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number.")
        
        if amount > self.__balance:
            return "The amount is too high. Choose a lower amount."
        
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        
        # Make dections from sender
        self.__balance -= amount
        self.transaction_history.append("Transfered {} to {} New balance: {}".format(amount, self.account_type, self.__balance))
        try:
            if isinstance(target_account, BankAccount):
                target_account.deposit(amount)
                target_account.transaction_history.append("Revieved {} from {} New balance: {}".format(amount,self.owner, target_account.__balance))
            else: print("Account does not exist")
        except ValueError:
            print("Target Account is not an instance of BankAccount class.")


        return f'Successfully transfered {amount} from {target_account.owner}.'
    
    def get_balance(self):
        return self.__balance


    def __str__(self):
        return f'Hello {self.owner}, your account balance is now {self.__balance}'
    