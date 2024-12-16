class BankAccount:
    def __init__(self, balance=0):
        self.__balance = balance

    def get_balance(self):
        return f"Current balance: {self.__balance}"

    def deposit(self, amount):
        self.__balance += amount
        return f"Current balance: {self.__balance}"

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        else:
            self.__balance -= amount
            return f"Current balance: {self.__balance}"

    def transfer(self, account, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        else:
            self.__balance -= amount
            account.deposit(amount)
            return f"Transferred {amount}, remaining balance: {self.__balance}"

    def __str__(self):
        return f"Current balance: {self.__balance}"

# Example input and output
# Creating the main account with an initial balance
balance = int(input("Enter initial account balance: "))  # Example: 1000
account1 = BankAccount(balance)

# Printing the current account balance
print(account1)

# Depositing into the account
deposit_amount = int(input("Enter amount to deposit: "))  # Example: 200
print(account1.deposit(deposit_amount))  # Output: Current balance: 1200

# Withdrawing from the account
withdraw_amount = int(input("Enter amount to withdraw: "))  # Example: 150
print(account1.withdraw(withdraw_amount))  # Output: Current balance: 1050

# Creating a second account and making a transfer
transfer_account_balance = int(input("Enter the balance of the second account: "))  # Example: 500
account2 = BankAccount(transfer_account_balance)

transfer_amount = int(input("Enter amount to transfer: "))  # Example: 300
print(account1.transfer(account2, transfer_amount))  # Output: Transferred 300, remaining balance: 750

# Printing the balance of the second account after the transfer
print(account2.get_balance())  # Output: Current balance: 800
