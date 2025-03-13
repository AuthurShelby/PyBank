import csv
import pandas as pd
from datetime import datetime

# Bank class
class PyBank:
    def __init__(self):
        self.name = 'PyBank'
        self.Accounts = {}  # Dictionary to store accounts

# Customer class (creates an account)
class Customer:
    def __init__(self, ClientName, PhoneNumber, Address, EmailAddress):
        self.ClientName = ClientName
        self.PhoneNumber = PhoneNumber
        self.Address = Address
        self.EmailAddress = EmailAddress
        self.AccountNumber = None  # Will be assigned when account is created
        self.InitialBalance = 0.0

    # Method to create an account
    def CreateAccount(self, bank: PyBank):

        self.AccountNumber = len(bank.Accounts) + 10001  # Unique account number
        bank.Accounts[self.AccountNumber] = Account(self.AccountNumber, self.InitialBalance)
        print(f'Account Created! --- Account Number: {self.AccountNumber}')

    # Display account details
    def AccountDetails(self, bank: PyBank):

        if self.AccountNumber in bank.Accounts:
            account = bank.Accounts[self.AccountNumber]
            print("\n==== ACCOUNT DETAILS ====")
            print(f'Account Number: {self.AccountNumber}')
            print(f'Balance: {account.Balance}')
            print('\nTransaction History:')
            account.DisplayTransactions()
            print("========================\n")
        else:
            print("No account found!")

# Account class (stores balance and transaction history)
class Account:

    def __init__(self, AccountNumber, Balance):
        self.AccountNumber = AccountNumber
        self.Balance = Balance
        self.Transactions = {'Account Number':None , 'Date & Time':None , 'Transaction Type':None , 'Amount': None}  # Store transaction history

    # Deposit function
    def deposit(self):
        try:
            AMOUNT = float(input('Enter an amount to deposit: '))
            if AMOUNT <= 0:
                print('Invalid amount! Please enter a positive value.')
                return
            
            self.Balance += AMOUNT
            # for Transaction details
            self.Transactions['Account Number'] = self.AccountNumber
            self.Transactions['Date & Time'] = datetime.now()
            self.Transactions['Transaction Type'] = self.withdraw.__name__
            self.Transactions['Amount'] = AMOUNT
            print(f'Amount Deposited! --- New Balance: {self.Balance}')
    
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

    # Withdraw function
    def withdraw(self):
        try:
            AMOUNT = float(input('Enter an amount to withdraw: '))
            if AMOUNT <= 0:
                print('Invalid amount! Please enter a positive value.')
                return
            if AMOUNT > self.Balance:
                print('Insufficient balance!')
                return

            self.Balance -= AMOUNT

            # for Transaction details
            self.Transactions['Account Number'] = self.AccountNumber
            self.Transactions['Date & Time'] = datetime.now()
            self.Transactions['Transaction Type'] = self.withdraw.__name__
            self.Transactions['Amount'] = AMOUNT

            print(f'Amount Withdrawn! --- New Balance: {self.Balance}')
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

    # Display transaction history
    def DisplayTransactions(self):

        if not self.Transactions:
            print("No transactions yet.")
        else:
            for key , values in self.Transactions.items():
                print(f'{key} -- {values}')

# ========== MAIN PROGRAM ==========
bank = PyBank()
customer1 = Customer("John Doe", "1234567890", "123 Street, City", "john@example.com")
customer1.CreateAccount(bank)  # Creating an account

account = bank.Accounts[customer1.AccountNumber]  # Get the account object

while True:
    print("\n==== PYBANK MENU ====")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. View Account Details")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        account.deposit()
    elif choice == "2":
        account.withdraw()
    elif choice == "3":
        customer1.AccountDetails(bank)
    elif choice == "4":
        print("Thank you for using PyBank! Goodbye.")
        break
    else:
        print("Invalid choice! Please enter a number between 1 and 4.")
