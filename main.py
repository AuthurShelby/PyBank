from datetime import datetime
import csv

# Bank class
class PyBank:
    def __init__(self):
        self.name = 'PyBank'
        self.Accounts = {}  # Dictionary to store accounts (Account Number → Account Object)
        self.Customers = {}  # Dictionary to store customers (Account Number → Customer Object)
        self.LoadAccountsFromCSV()  # Load existing accounts when the program starts
        
    # For account section 
    def SaveAccountsToCSV(self):
        with open('accounts.csv', mode='w', newline='') as file:
            fieldnames = ["AccountNumber", "ClientName", "PhoneNumber", "Address", "EmailAddress", "Balance"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            print(self.Customers.items())
            for acc_num, cust in self.Customers.items():
                account = self.Accounts[acc_num]
                writer.writerow({
                    "AccountNumber": acc_num,
                    "ClientName": cust.ClientName,
                    "PhoneNumber": cust.PhoneNumber,
                    "Address": cust.Address,
                    "EmailAddress": cust.EmailAddress,
                    "Balance": account.Balance
                })
    # For Loading the account
    def LoadAccountsFromCSV(self):
        try:
            with open('accounts.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    customer = Customer(row["ClientName"], row["PhoneNumber"], row["Address"], row["EmailAddress"])
                    customer.AccountNumber = int(row["AccountNumber"])
                    account = Account(customer.AccountNumber, float(row["Balance"]))

                    self.Customers[customer.AccountNumber] = customer
                    self.Accounts[customer.AccountNumber] = account
        except FileNotFoundError:
            pass  # If no file exists, start fresh

# Customer class (creates an account)
class Customer:
    def __init__(self, ClientName, PhoneNumber, Address, EmailAddress):
        self.ClientName = ClientName
        self.PhoneNumber = PhoneNumber
        self.Address = Address
        self.EmailAddress = EmailAddress
        self.AccountNumber = None  # Will be assigned when an account is created
        self.InitialBalance = 0.0

    # Method to create an account
    def CreateAccount(self, bank: PyBank):
        self.AccountNumber = len(bank.Accounts) + 10010  # Generate unique account number
        bank.Accounts[self.AccountNumber] = Account(self.AccountNumber, self.InitialBalance)
        bank.Customers[self.AccountNumber] = self  # Store customer details
        bank.SaveAccountsToCSV()  # Save new account to file
        print(f'\n Account Created! --- Account Number: {self.AccountNumber}\n')

    # Display account details
    def AccountDetails(self, bank: PyBank):
        if self.AccountNumber in bank.Accounts:
            account = bank.Accounts[self.AccountNumber]
            print("\n==== ACCOUNT DETAILS ====")
            print(f'Account Number: {self.AccountNumber}')
            print(f'Customer Name: {self.ClientName}')
            print(f'Balance: {account.Balance}')
            print('\nTransaction History:')
            account.DisplayTransactions()
            print("========================\n")
        else:
            print(" No account found!")

# Account class (stores balance and transaction history)
class Account:
    def __init__(self, AccountNumber, Balance):
        self.AccountNumber = AccountNumber
        self.Balance = Balance
        self.Transactions = []  # Store transaction history

    # Deposit function
    def deposit(self, bank: PyBank):
        try:
            AMOUNT = float(input('Enter an amount to deposit: '))
            if AMOUNT <= 0:
                print(' Invalid amount! Please enter a positive value.')
                return
            
            self.Balance += AMOUNT
            self.Transactions.append(f'{datetime.now()} :: {self.AccountNumber} --- Deposited: {AMOUNT}')
            bank.SaveAccountsToCSV()  # Save changes
            print(f' Amount Deposited! --- New Balance: {self.Balance}')
        except ValueError:
            print(" Invalid input! Please enter a numeric value.")

    # Withdraw function
    def withdraw(self, bank: PyBank):
        try:
            AMOUNT = float(input('Enter an amount to withdraw: '))
            if AMOUNT <= 0:
                print(' Invalid amount! Please enter a positive value.')
                return
            if AMOUNT > self.Balance:
                print(' Insufficient balance!')
                return

            self.Balance -= AMOUNT
            self.Transactions.append(f'{datetime.now()} :: {self.AccountNumber} --- Withdrawn: {AMOUNT}')
            bank.SaveAccountsToCSV()  # Save changes
            print(f' Amount Withdrawn! --- New Balance: {self.Balance}')
        except ValueError:
            print(" Invalid input! Please enter a numeric value.")

    # Display transaction history
    def DisplayTransactions(self):
        if not self.Transactions:
            print("No transactions yet.")
        else:
            for trans in self.Transactions:
                print(trans)

# ========== MAIN PROGRAM ==========
bank = PyBank()

while True:
    print("\n==== PYBANK MENU ====")
    print("1. Create New Account")
    print("2. Select an Existing Account")
    print("3. Exit")
    main_choice = int(input("Enter your choice: "))

    if main_choice == 1:
        name = input("Enter your name: ")
        phone = int(input("Enter your phone number: "))
        address = input("Enter your address: ")
        email = input("Enter your email: ")
        
        new_customer = Customer(name, phone, address, email)
        new_customer.CreateAccount(bank)

    elif main_choice == 2:
        acc_number = int(input("Enter your account number: "))

        if acc_number in bank.Accounts:
            customer = bank.Customers[acc_number]
            account = bank.Accounts[acc_number]

            while True:
                print("\n==== ACCOUNT MENU ====")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. View Account Details")
                print("4. Logout (Return to Main Menu)")
                acc_choice = int(input("Enter your choice: "))

                if acc_choice == 1:
                    account.deposit(bank)
                elif acc_choice == 2:
                    account.withdraw(bank)
                elif acc_choice == 3:
                    customer.AccountDetails(bank)
                elif acc_choice == 4:
                    print(" Logging out... Returning to Main Menu.\n")
                    break
                else:
                    print(" Invalid choice! Please enter a number between 1 and 4.")
        else:
            print(" Account not found! Please enter a valid account number.")

    elif main_choice == 3:
        print(" Thank you for using PyBank! Goodbye.")
        break
    else:
        print(" Invalid choice! Please enter a number between 1 and 3.")
