import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk


class AdminModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Admin Module")
        self.window.geometry("600x400")
        self.center_window()
        self.window.resizable(False, False)

        self.treeview = ttk.Treeview(self.window)
        self.treeview.pack(pady=10, padx=10)

        self.treeview["columns"] = ("username", "first_name", "last_name", "initial_amount")

        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("username", anchor=tk.W, width=100)
        self.treeview.column("first_name", anchor=tk.W, width=100)
        self.treeview.column("last_name", anchor=tk.W, width=100)
        self.treeview.column("initial_amount", anchor=tk.W, width=100)

        self.treeview.heading("#0", text="", anchor=tk.W)
        self.treeview.heading("username", text="Username", anchor=tk.W)
        self.treeview.heading("first_name", text="First Name", anchor=tk.W)
        self.treeview.heading("last_name", text="Last Name", anchor=tk.W)
        self.treeview.heading("initial_amount", text="Initial Amount", anchor=tk.W)

        self.load_data()

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add", command=self.add_entry)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit", command=self.edit_entry)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_entry)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def center_window(self):
        window_width = self.window.winfo_reqwidth()
        window_height = self.window.winfo_reqheight()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f"+{x}+{y}")

    def load_data(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="banking"
            )
            cursor = db.cursor()

            query = """
            SELECT tbl_login.username, tbl_account.first_name, tbl_account.last_name, tbl_account.initial_amount
            FROM tbl_login
            INNER JOIN tbl_account ON tbl_login.user_id = tbl_account.user_id
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Clear existing items in treeview
            self.treeview.delete(*self.treeview.get_children())

            # Insert data into treeview
            for row in rows:
                self.treeview.insert("", tk.END, values=row)

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))
        finally:
            if 'db' in locals() or 'db' in globals():
                db.close()

    def add_entry(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Add Entry")
        add_window.geometry("300x200")
        self.center_window(add_window)
        add_window.resizable(False, False)

        username_label = tk.Label(add_window, text="Username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(add_window)
        username_entry.pack(pady=5)

        first_name_label = tk.Label(add_window, text="First Name:")
        first_name_label.pack(pady=5)
        first_name_entry = tk.Entry(add_window)
        first_name_entry.pack(pady=5)

        last_name_label = tk.Label(add_window, text="Last Name:")
        last_name_label.pack(pady=5)
        last_name_entry = tk.Entry(add_window)
        last_name_entry.pack(pady=5)

        initial_amount_label = tk.Label(add_window, text="Initial Amount:")
        initial_amount_label.pack(pady=5)
        initial_amount_entry = tk.Entry(add_window)
        initial_amount_entry.pack(pady=5)

        add_button = tk.Button(add_window, text="Add", command=lambda: self.insert_entry(
            username_entry.get(),
            first_name_entry.get(),
            last_name_entry.get(),
            initial_amount_entry.get(),
            add_window
        ))
        add_button.pack(pady=10)

    def insert_entry(self, username, first_name, last_name, initial_amount, add_window):
        if not username or not first_name or not last_name or not initial_amount:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="banking"
            )
            cursor = db.cursor()

            # Insert into tbl_login
            login_query = "INSERT INTO tbl_login (username) VALUES (%s)"
            login_values = (username,)
            cursor.execute(login_query, login_values)
            db.commit()

            user_id = cursor.lastrowid

            # Insert into tbl_account
            account_query = "INSERT INTO tbl_account (user_id, first_name, last_name, initial_amount) VALUES (%s, %s, %s, %s)"
            account_values = (user_id, first_name, last_name, initial_amount)
            cursor.execute(account_query, account_values)
            db.commit()

            messagebox.showinfo("Success", "Entry added successfully!")

            # Refresh treeview
            self.load_data()

            # Close add window
            add_window.destroy()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))
        finally:
            if 'db' in locals() or 'db' in globals():
                db.close()

    def edit_entry(self):
        selected_item = self.treeview.focus()

        if not selected_item:
            messagebox.showerror("Error", "No entry selected.")
            return

        values = self.treeview.item(selected_item)["values"]

        if not values:
            return

        username = values[0]
        first_name = values[1]
        last_name = values[2]
        initial_amount = values[3]

        edit_window = tk.Toplevel(self.window)
        edit_window.title("Edit Entry")
        edit_window.geometry("300x200")
        self.center_window(edit_window)
        edit_window.resizable(False, False)

        username_label = tk.Label(edit_window, text="Username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(edit_window)
        username_entry.insert(tk.END, username)
        username_entry.pack(pady=5)

        first_name_label = tk.Label(edit_window, text="First Name:")
        first_name_label.pack(pady=5)
        first_name_entry = tk.Entry(edit_window)
        first_name_entry.insert(tk.END, first_name)
        first_name_entry.pack(pady=5)

        last_name_label = tk.Label(edit_window, text="Last Name:")
        last_name_label.pack(pady=5)
        last_name_entry = tk.Entry(edit_window)
        last_name_entry.insert(tk.END, last_name)
        last_name_entry.pack(pady=5)

        initial_amount_label = tk.Label(edit_window, text="Initial Amount:")
        initial_amount_label.pack(pady=5)
        initial_amount_entry = tk.Entry(edit_window)
        initial_amount_entry.insert(tk.END, initial_amount)
        initial_amount_entry.pack(pady=5)

        save_button = tk.Button(edit_window, text="Save", command=lambda: self.update_entry(
            selected_item,
            username_entry.get(),
            first_name_entry.get(),
            last_name_entry.get(),
            initial_amount_entry.get(),
            edit_window
        ))
        save_button.pack(pady=10)

    def update_entry(self, selected_item, username, first_name, last_name, initial_amount, edit_window):
        if not selected_item:
            messagebox.showerror("Error", "No entry selected.")
            return

        if not username or not first_name or not last_name or not initial_amount:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        values = self.treeview.item(selected_item)["values"]
        user_id = values[0]

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="banking"
            )
            cursor = db.cursor()

            # Update tbl_login
            login_query = "UPDATE tbl_login SET username = %s WHERE user_id = %s"
            login_values = (username, user_id)
            cursor.execute(login_query, login_values)
            db.commit()

            # Update tbl_account
            account_query = "UPDATE tbl_account SET first_name = %s, last_name = %s, initial_amount = %s WHERE user_id = %s"
            account_values = (first_name, last_name, initial_amount, user_id)
            cursor.execute(account_query, account_values)
            db.commit()

            messagebox.showinfo("Success", "Entry updated successfully!")

            # Refresh treeview
            self.load_data()

            # Close edit window
            edit_window.destroy()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))
        finally:
            if 'db' in locals() or 'db' in globals():
                db.close()

    def delete_entry(self):
        selected_item = self.treeview.focus()

        if not selected_item:
            messagebox.showerror("Error", "No entry selected.")
            return

        values = self.treeview.item(selected_item)["values"]
        user_id = values[0]

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this entry?")

        if confirm:
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="banking"
                )
                cursor = db.cursor()

                # Delete from tbl_account
                account_query = "DELETE FROM tbl_account WHERE user_id = %s"
                account_values = (user_id,)
                cursor.execute(account_query, account_values)
                db.commit()

                # Delete from tbl_login
                login_query = "DELETE FROM tbl_login WHERE user_id = %s"
                login_values = (user_id,)
                cursor.execute(login_query, login_values)
                db.commit()

                messagebox.showinfo("Success", "Entry deleted successfully!")

                # Refresh treeview
                self.load_data()

            except mysql.connector.Error as error:
                messagebox.showerror("Database Error", str(error))
            finally:
                if 'db' in locals() or 'db' in globals():
                    db.close()

        def load_data(self):
            self.treeview.delete(*self.treeview.get_children())

            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="banking"
                )
                cursor = db.cursor()

                query = """
                       SELECT tbl_account.user_id, tbl_login.username, tbl_account.first_name, tbl_account.last_name,
                       tbl_account.initial_amount
                       FROM tbl_account
                       INNER JOIN tbl_login ON tbl_account.user_id = tbl_login.user_id
                   """
                cursor.execute(query)
                data = cursor.fetchall()

                for row in data:
                    self.treeview.insert("", tk.END, values=row)

            except mysql.connector.Error as error:
                messagebox.showerror("Database Error", str(error))
            finally:
                if 'db' in locals() or 'db' in globals():
                    db.close()

            def center_window(self, window):
                window_width = window.winfo_reqwidth()
                window_height = window.winfo_reqheight()
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()
                x = int((screen_width / 2) - (window_width / 2))
                y = int((screen_height / 2) - (window_height / 2))
                window.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    window = tk.Tk()
    admin_module = AdminModule(window)
    window.mainloop()
