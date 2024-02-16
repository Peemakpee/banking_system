import datetime
import tkinter as tk
from tkinter import messagebox

import mysql.connector


def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="banking"
    )


def center_window(window):
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"+{x}+{y}")


class BankingSystem:
    def __init__(self, user_id, login_window):
        self.user_id = user_id
        self.login_window = login_window
        self.window = tk.Tk()
        self.window.title("Banking System")
        self.window.geometry("300x280")
        center_window(self.window)
        self.window.resizable(False, False)
        self.window.configure(bg="#f0f0f0")

        self.account_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.account_frame.pack(pady=10)

        self.name_label = tk.Label(self.account_frame, text="", bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.name_label.pack()

        self.balance_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.balance_frame.pack(pady=10)

        self.balance_label = tk.Label(self.balance_frame, text="Balance:", bg="#f0f0f0", font=("Arial", 12))
        self.balance_label.pack()
        self.balance_value = tk.Label(self.balance_frame, text="", bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.balance_value.pack()

        self.transaction_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.transaction_frame.pack(pady=10)

        self.deposit_frame = tk.Frame(self.transaction_frame, bg="#f0f0f0")
        self.deposit_frame.pack(side=tk.LEFT, padx=10)

        self.deposit_label = tk.Label(self.deposit_frame, text="Deposit Amount:", bg="#f0f0f0", font=("Arial", 10))
        self.deposit_label.pack()
        self.deposit_entry = tk.Entry(self.deposit_frame, font=("Arial", 10))
        self.deposit_entry.pack()

        self.deposit_button = tk.Button(self.deposit_frame, text="Deposit", command=self.deposit, bg="#2196f3", fg="white", relief=tk.FLAT, font=("Arial", 10, "bold"))
        self.deposit_button.pack()

        self.withdraw_frame = tk.Frame(self.transaction_frame, bg="#f0f0f0")
        self.withdraw_frame.pack(side=tk.RIGHT, padx=10)

        self.withdraw_label = tk.Label(self.withdraw_frame, text="Withdraw Amount:", bg="#f0f0f0", font=("Arial", 10))
        self.withdraw_label.pack()
        self.withdraw_entry = tk.Entry(self.withdraw_frame, font=("Arial", 10))
        self.withdraw_entry.pack()

        self.withdraw_button = tk.Button(self.withdraw_frame, text="Withdraw", command=self.withdraw, bg="#4caf50", fg="white", relief=tk.FLAT, font=("Arial", 10, "bold"))
        self.withdraw_button.pack()

        self.end_transaction_button = tk.Button(self.window, text="End Transaction", command=self.end_transaction, bg="#f44336", fg="white", relief=tk.FLAT, font=("Arial", 10, "bold"))
        self.end_transaction_button.pack(pady=10, anchor=tk.S)

        self.refresh_account_info()

        self.date_time_label = tk.Label(self.window, text="", bg="#f0f0f0", font=("Arial", 10))
        self.date_time_label.pack(anchor=tk.NE, padx=10, pady=5)

        self.update_date_time()

    def refresh_account_info(self):
        try:
            db = connect_to_database()
            cursor = db.cursor()
            query = "SELECT first_name, last_name FROM tbl_account WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            first_name, last_name = result

            self.name_label.config(text=f"{first_name} {last_name}")
            query = "SELECT initial_amount FROM tbl_account WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            balance = result[0]
            self.balance_value.config(text=str(balance))
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "An error occurred during the database operation: " + str(e))
        finally:
            if 'db' in locals() or 'db' in globals():
                db.close()

    def end_transaction(self):
        self.window.destroy()
        self.login_window.open_login_window()

    def withdraw(self):
        amount = self.withdraw_entry.get()
        if not amount:
            messagebox.showerror("Error", "Please enter an amount.")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Please enter a valid amount.")
                self.clear_fields()
                return

            db = connect_to_database()
            cursor = db.cursor()

            # Retrieve current balance
            query = "SELECT initial_amount FROM tbl_account WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            balance = result[0]

            if amount > balance:
                messagebox.showerror("Error", "Insufficient balance.")
                return

            # Update balance
            new_balance = balance - amount
            update_query = "UPDATE tbl_account SET initial_amount = %s WHERE user_id = %s"
            cursor.execute(update_query, (new_balance, self.user_id))
            db.commit()

            self.refresh_balance()
            messagebox.showinfo("Withdraw", "Withdrawal successful.")
            self.clear_fields()

        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            self.clear_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "An error occurred during the database operation: " + str(e))
        finally:
            if 'db' in locals() or 'db' in globals():
                db.close()

    def deposit(self):
        amount = self.deposit_entry.get()
        if not amount:
            messagebox.showerror("Error", "Please enter an amount.")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Please enter a valid amount.")
                self.clear_fields()
                return

            db = connect_to_database()
            cursor = db.cursor()

            # Retrieve current balance
            query = "SELECT initial_amount FROM tbl_account WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            balance = result[0]

            # Update balance
            new_balance = balance + amount
            update_query = "UPDATE tbl_account SET initial_amount = %s WHERE user_id = %s"
            cursor.execute(update_query, (new_balance, self.user_id))
            db.commit()

            self.refresh_balance()
            messagebox.showinfo("Deposit", "Deposit successful.")
            self.clear_fields()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            self.clear_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "An error occurred during the database operation: " + str(e))
        finally:
            if 'db' in locals() or 'db' in globals():
                db.close()

    def refresh_balance(self):
        try:
            db = connect_to_database()
            cursor = db.cursor()
            query = "SELECT initial_amount FROM tbl_account WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            balance = result[0]
            self.balance_value.config(text=str(balance))

        except mysql.connector.Error as e:
            messagebox.showerror("Error", "An error occurred during the database operation: " + str(e))
        finally:
            if 'db' in locals() or 'db' in globals():
                db.close()

    def clear_fields(self):
        self.withdraw_entry.delete(0, tk.END)
        self.deposit_entry.delete(0, tk.END)

    def update_date_time(self):
        now = datetime.datetime.now()
        formatted_date = now.strftime("Today is %A, %B %d, %Y")
        formatted_time = now.strftime("%I:%M:%S %p")
        date_time_string = f"{formatted_date}  {formatted_time}"
        self.date_time_label.config(text=date_time_string)
        self.date_time_label.after(1000, self.update_date_time)