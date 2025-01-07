class BankAccount:
    def __init__(self, owner, balance=0, account_type = "Checking"):
        if account_type not in  ("Checking", "Savings"):
            raise ValueError("Account_type must either be Checking or Savings account")
        self.account_type = account_type
        self.transaction_history = []
        self.owner = owner
        if not isinstance(balance, (int, float)) or balance < 0:
            raise ValueError("Balance must be a non-negative number.")
        self.__balance = balance  # Private attribute


    def deposit(self, amount):
        self.transaction_history.append('Current balance: {}'.format(self.__balance))
        try:
            if amount <= 0:
                print("Enter a valid amount.")
            else:
                self.__balance += amount
                print("You have deposited {}".format(amount))
                self.transaction_history.append("Deposit: {}. New balance:{}".format(amount, self.__balance))
        except TypeError:
            print('Deposit must be a number')

    def withdraw(self, amount):
        self.transaction_history.append('Current Balance: {}'.format(self.__balance))
        try:
            if self.__balance < amount:
                print("Insufficient funds to make withdrawal.")
            elif amount <= 0:
                print("Please enter a valid amount")
            else:
                if self.account_type == "Savings":
                    if self.__balance - amount < 100:
                        print("Please withdraw a lower amount")
                    else:
                        self.__balance -= amount
                        self.transaction_history.append("Savings Withdrawal: {}. New Savings balance: {}".format(amount, self.__balance))
                else:
                    self.__balance -= amount
                    print("Checking Withdrawal: {}".format(amount))
                    self.transaction_history.append("Checking Withdrawal: {}. New Checking balance: {}".format(amount, self.__balance))
                
        except TypeError:
                print("Entry must be a number.")

    def transfer(self, amount, target_account):
        if amount > self.__balance:
            print("The amount is too high. Choose a lower amount.")
        else:
            target_account.deposit(amount)
            self.transaction_history.append("Transfered {} to {} New balance: {}".format(amount, self.owner, self.__balance))
            self.transaction_history.append("Revieved {} from {} New balance: {}".format(amount,self.owner, target_account.__balance))

    def __str__(self):
        return f'Hello {self.owner}, your account balance is now: {self.__balance}'