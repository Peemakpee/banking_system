import tkinter as tk
from tkinter import messagebox

import mysql.connector

from BankingModule import BankingSystem
from RegisterModule import RegisterWindow


def center_window(window):
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"+{x}+{y}")


class LoginWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Login")
        self.window.geometry("250x150")
        center_window(self.window)
        self.window.resizable(False, False)
        self.window.configure(bg="#f0f0f0")

        # Create a frame to hold the labels and entry fields
        self.form_frame = tk.Frame(window, pady=10, bg="#f0f0f0")
        self.form_frame.pack()

        self.username_label = tk.Label(self.form_frame, text="Username:", bg="#f0f0f0", font=("Arial", 10))
        self.username_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = tk.Entry(self.form_frame, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.form_frame, text="Password:", bg="#f0f0f0", font=("Arial", 10))
        self.password_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(self.form_frame, show="*", font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(window, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        self.login_button = tk.Button(self.button_frame, text="Login", command=self.validate_login, bg="#4caf50", fg="white", relief=tk.FLAT, font=("Arial", 10, "bold"))
        self.login_button.pack(side="left", padx=5)

        self.register_button = tk.Button(self.button_frame, text="Register", command=self.open_register_window, bg="#2196f3", fg="white", relief=tk.FLAT, font=("Arial", 10, "bold"))
        self.register_button.pack(side="left", padx=5)

        self.register_window = None

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="banking"
            )
            cursor = db.cursor()

            # Check if the credentials match the admin account in tbl_admin
            query = "SELECT * FROM tbl_admin WHERE BINARY username = %s AND BINARY password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Login", "Login successful as admin.")
                self.open_admin_module()
                self.clear_fields()
            else:
                # If not an admin, check if the credentials match a regular user in tbl_login
                query = "SELECT * FROM tbl_login WHERE BINARY username = %s AND BINARY password = %s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()

                if result:
                    messagebox.showinfo("Login", "Login successful.")
                    self.open_banking_system(result[0])
                    self.clear_fields()
                else:
                    messagebox.showerror("Error", "Invalid username or password.")
                    self.clear_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "An error occurred during the database operation: " + str(e))

    def open_admin_module(self):
        admin_window = tk.Toplevel(self.window)
        from AdminModule import AdminModule
        admin_module = AdminModule(admin_window)
        self.window.withdraw()

    def open_register_window(self):
        register_window = tk.Toplevel(self.window)
        self.register_window = RegisterWindow(register_window, self)
        self.window.withdraw()

    def open_banking_system(self, user_id):
        banking_system = BankingSystem(user_id, self)
        self.window.withdraw()

    def open_login_window(self):
        self.window.deiconify()

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


if __name__ == "__main__":
    try:
        window = tk.Tk()
        from AdminModule import AdminModule
        login_module = LoginWindow(window)
        window.mainloop()

    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred: " + str(e))
