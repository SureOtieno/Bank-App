class BankAccount:
    def __init__(self, owner, balance=0, transaction_history = [], account_type = "Checking"):
        if account_type not in  ("Checking", "Savings"):
            raise ValueError("Account_type must either be Checking or Savings account")
        self.account_type = account_type
        self.transaction_history = transaction_history
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

# # # Creating an account
# # sules_account = BankAccount("Suleiman", 5000)
# # nimas_account = BankAccount("Suleiman", 5000)

# # # Making transactions
# # sules_account.deposit(5000)         # Balance becomes 1500
# # sules_account.withdraw(100)       # Should print an error
# # sules_account.withdraw(200)
# # sules_account.deposit(2000)
# # sules_account.transfer(200, nimas_account)

# # print(sules_account.transaction_history)
# # print(nimas_account.transaction_history)

# # Test the BankAccount class
# account1 = BankAccount("John", 500, account_type="Checking")
# account2 = BankAccount("Alice", 300, account_type="Savings")

# # Initial state
# print(account1)  # Expect: Hello John, your Checking account balance is now: 500
# print(account2)  # Expect: Hello Alice, your Savings account balance is now: 300

# # Deposit into account1
# account1.deposit(100)  # Expect: "You have deposited 100. New balance: 600"

# # Withdraw from account2
# account2.withdraw(50)  # Expect: "You have withdrawn 50. New balance: 250"

# # Attempt to withdraw more than balance in account2
# account2.withdraw(500)  # Expect: "Insufficient funds to make withdrawal."

# # Attempt to withdraw below minimum in savings
# account2.withdraw(200)  # Expect: "Savings account must maintain a minimum balance of $100."

# # Transfer from account1 to account2
# account1.transfer(200, account2)
# # Expect:
# # "Transferred 200 to Alice. Your new balance: 400"
# # In account2, expect: "Received 200 from John. New balance: 450"

# # Attempt invalid transfer
# account1.transfer(500, account2)  # Expect: "Insufficient funds to make transfer."

# # Print transaction histories
# print("\nTransaction History for John:")
# print(account1.transaction_history)

# print("\nTransaction History for Alice:")
# print(account2.transaction_history)
