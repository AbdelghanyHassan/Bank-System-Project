import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import json
import os

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, password):
    """Check if a password matches the hashed password."""
    return hashed_password == hash_password(password)

def save_accounts(accounts):
    """Save all accounts to a JSON file."""
    with open("accounts.json", "w") as file:
        json.dump([acc.get_account_info() for acc in accounts], file)

def load_accounts():
    """Load all accounts from a JSON file."""
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as file:
            accounts_data = json.load(file)
            return [BankAccount(**acc) for acc in accounts_data]
    return []

class BankAccount:
    def __init__(self, account_number, account_holder, password, balance=0.0, account_type="Savings"):
        self.account_number = account_number
        self.account_holder = account_holder
        self.password = hash_password(password)  # Store hashed password
        self.balance = balance
        self.account_type = account_type
        self.transactions = []  # To store transaction history

    def check_password(self, password):
        """Check if the provided password matches the stored hashed password."""
        return check_password(self.password, password)

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposit: {amount}")
            return True, f"Deposit successful! New balance: {self.balance}"
        return False, "Invalid deposit amount."

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdraw: {amount}")
            return True, f"Withdrawal successful! New balance: {self.balance}"
        return False, "Invalid withdrawal amount or insufficient balance."

    def check_balance(self):
        """Return the current balance."""
        return f"Account balance: {self.balance}"

    def get_account_info(self):
        """Return account details as a dictionary."""
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "balance": self.balance,
            "account_type": self.account_type,
            "transactions": self.transactions
        }

class BankSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank System")
        self.accounts = load_accounts()
        self.current_account = None

        # Main Menu
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20)

        tk.Button(self.menu_frame, text="Create an Account", command=self.show_create_account).pack(pady=10)
        tk.Button(self.menu_frame, text="Login to an Account", command=self.show_login).pack(pady=10)
        tk.Button(self.menu_frame, text="Exit", command=self.exit_system).pack(pady=10)

        # Create Account Frame
        self.create_account_frame = tk.Frame(self.root)
        tk.Label(self.create_account_frame, text="Account Number").grid(row=0, column=0)
        tk.Label(self.create_account_frame, text="Account Holder").grid(row=1, column=0)
        tk.Label(self.create_account_frame, text="Password").grid(row=2, column=0)
        tk.Label(self.create_account_frame, text="Account Type").grid(row=3, column=0)

        self.acc_num_entry = tk.Entry(self.create_account_frame)
        self.acc_holder_entry = tk.Entry(self.create_account_frame)
        self.password_entry = tk.Entry(self.create_account_frame, show='*')
        self.account_type_var = tk.StringVar(value="Savings")
        tk.Radiobutton(self.create_account_frame, text="Savings", variable=self.account_type_var, value="Savings").grid(row=3, column=1, sticky="w")
        tk.Radiobutton(self.create_account_frame, text="Checking", variable=self.account_type_var, value="Checking").grid(row=4, column=1, sticky="w")

        self.acc_num_entry.grid(row=0, column=1)
        self.acc_holder_entry.grid(row=1, column=1)
        self.password_entry.grid(row=2, column=1)

        tk.Button(self.create_account_frame, text="Create Account", command=self.create_account).grid(row=5, column=1, pady=10)
        tk.Button(self.create_account_frame, text="Back to Menu", command=self.show_menu).grid(row=6, column=1)

        # Login Frame
        self.login_frame = tk.Frame(self.root)
        tk.Label(self.login_frame, text="Account Number").grid(row=0, column=0)
        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)

        self.login_acc_num_entry = tk.Entry(self.login_frame)
        self.login_password_entry = tk.Entry(self.login_frame, show='*')

        self.login_acc_num_entry.grid(row=0, column=1)
        self.login_password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=1, pady=10)
        tk.Button(self.login_frame, text="Back to Menu", command=self.show_menu).grid(row=3, column=1)

        # Main UI
        self.main_frame = tk.Frame(self.root)
        tk.Button(self.main_frame, text="Deposit", command=self.deposit).pack(pady=10)
        tk.Button(self.main_frame, text="Withdraw", command=self.withdraw).pack(pady=10)
        tk.Button(self.main_frame, text="Check Balance", command=self.check_balance).pack(pady=10)
        tk.Button(self.main_frame, text="Account Info", command=self.show_account_info).pack(pady=10)
        tk.Button(self.main_frame, text="Logout", command=self.show_menu).pack(pady=10)

        self.show_menu()

    def show_menu(self):
        """Display the main menu."""
        self.create_account_frame.pack_forget()
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        self.menu_frame.pack(pady=20)

    def show_create_account(self):
        """Display the create account frame."""
        self.menu_frame.pack_forget()
        self.create_account_frame.pack(pady=20)

    def show_login(self):
        """Display the login frame."""
        self.menu_frame.pack_forget()
        self.login_frame.pack(pady=20)

    def create_account(self):
        """Create a new account and save it."""
        account_number = self.acc_num_entry.get()
        account_holder = self.acc_holder_entry.get()
        password = self.password_entry.get()

        if any(account.account_number == account_number for account in self.accounts):
            messagebox.showerror("Error", "Account number already exists. Try a different number.")
            return

        account_type = self.account_type_var.get()
        self.accounts.append(BankAccount(account_number, account_holder, password, account_type=account_type))
        save_accounts(self.accounts)
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_menu()

    def login(self):
        """Login to an existing account."""
        account_number = self.login_acc_num_entry.get()
        password = self.login_password_entry.get()

        account = next((acc for acc in self.accounts if acc.account_number == account_number), None)
        if account and account.check_password(password):
            self.current_account = account
            self.show_main()
        else:
            messagebox.showerror("Error", "Incorrect account number or password.")

    def show_main(self):
        """Display the main functionality frame."""
        self.login_frame.pack_forget()
        self.main_frame.pack(pady=20)

    def deposit(self):
        """Deposit money into the current account."""
        amount = float(self.prompt("Enter deposit amount:"))
        success, message = self.current_account.deposit(amount)
        messagebox.showinfo("Result", message)
        save_accounts(self.accounts)

    def withdraw(self):
        """Withdraw money from the current account."""
        amount = float(self.prompt("Enter withdrawal amount:"))
        success, message = self.current_account.withdraw(amount)
        messagebox.showinfo("Result", message)
        save_accounts(self.accounts)

    def check_balance(self):
        """Check the balance of the current account."""
        messagebox.showinfo("Balance", self.current_account.check_balance())

    def show_account_info(self):
        """Display the current account's information."""
        info = self.current_account.get_account_info()
        info_text = (f"Account Number: {info['account_number']}\n"
                     f"Account Holder: {info['account_holder']}\n"
                     f"Balance: {info['balance']}\n"
                     f"Account Type: {info['account_type']}\n"
                     f"Transactions:\n" + "\n".join(info['transactions']))
        messagebox.showinfo("Account Info", info_text)

    def prompt(self, prompt_text):
        """Display a prompt dialog and return the input value."""
        return simpledialog.askstring("Input", prompt_text)

    def exit_system(self):
        """Exit the application."""
        self.root.quit()

# Create the main window and run the application
root = tk.Tk()
