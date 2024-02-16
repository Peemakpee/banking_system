import tkinter as tk
from tkinter import messagebox

import mysql.connector


def center_window(window):
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"+{x}+{y}")


class RegisterWindow:
    def __init__(self, window, login_window):
        self.window = window
        self.login_window = login_window
        self.window.title("Register")
        self.window.geometry("280x280")
        center_window(self.window)
        self.window.resizable(False, False)
        self.window.configure(bg="#f0f0f0")

        self.form_frame = tk.Frame(window, pady=10, bg="#f0f0f0")
        self.form_frame.pack()

        self.username_label = tk.Label(self.form_frame, text="Username:", bg="#f0f0f0")
        self.username_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = tk.Entry(self.form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.form_frame, text="Password:", bg="#f0f0f0")
        self.password_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(self.form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.confirm_password_label = tk.Label(self.form_frame, text="Confirm Password:", bg="#f0f0f0")
        self.confirm_password_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.confirm_password_entry = tk.Entry(self.form_frame, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.first_name_label = tk.Label(self.form_frame, text="First Name:", bg="#f0f0f0")
        self.first_name_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.first_name_entry = tk.Entry(self.form_frame)
        self.first_name_entry.grid(row=3, column=1, padx=5, pady=5)

        self.last_name_label = tk.Label(self.form_frame, text="Last Name:", bg="#f0f0f0")
        self.last_name_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.last_name_entry = tk.Entry(self.form_frame)
        self.last_name_entry.grid(row=4, column=1, padx=5, pady=5)

        self.initial_amount_label = tk.Label(self.form_frame, text="Initial Amount:", bg="#f0f0f0")
        self.initial_amount_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.initial_amount_entry = tk.Entry(self.form_frame)
        self.initial_amount_entry.grid(row=5, column=1, padx=5, pady=5)

        self.button_frame = tk.Frame(window, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        self.register_button = tk.Button(self.button_frame, text="Register", command=self.register, bg="#2196f3", fg="white", relief=tk.FLAT)
        self.register_button.pack(side="left", padx=5)

        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel, bg="#f44336", fg="white", relief=tk.FLAT)
        self.cancel_button.pack(side="left", padx=5)

    def register(self):
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            first_name = self.first_name_entry.get()
            last_name = self.last_name_entry.get()
            initial_amount = self.initial_amount_entry.get()

            if not username or not password or not confirm_password or not first_name or not last_name or not initial_amount:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="banking"
            )
            cursor = db.cursor()

            login_query = "INSERT INTO tbl_login (username, password) VALUES (%s, %s)"
            login_values = (username, password)

            cursor.execute(login_query, login_values)
            db.commit()

            user_id = cursor.lastrowid

            account_query = "INSERT INTO tbl_account (user_Id, first_name, last_name, initial_amount) VALUES (%s, %s, %s, %s)"
            account_values = (user_id, first_name, last_name, initial_amount)

            cursor.execute(account_query, account_values)
            db.commit()

            messagebox.showinfo("Registration Successful", "User registered successfully!")
            self.clear_fields()
            self.cancel()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))
        finally:
            if 'db' in locals() or 'db' in globals():
                db.close()

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.initial_amount_entry.delete(0, tk.END)

    def cancel(self):
        self.window.destroy()
        self.login_window.open_login_window()


if __name__ == "__main__":
    window = tk.Tk()
    register_module = RegisterWindow(window)
    window.mainloop()
