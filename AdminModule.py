import tkinter as tk
from tkinter import ttk, messagebox

import mysql.connector


class AdminModule:
    def __init__(self, window):
        self.window = window
        self.window.title("Admin Control Panel")
        self.window.resizable(False, False)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="banking"
        )
        self.cursor = self.conn.cursor()

        self.create_treeview()
        self.create_form()
        self.populate_treeview()
        self.treeview.bind("<<TreeviewSelect>>", self.populate_form)

    def create_treeview(self):
        self.treeview = ttk.Treeview(self.window, columns=("Username", "First Name", "Last Name", "Initial Amount"),
                                     style="Treeview")
        self.treeview.heading("#0", text="User ID")
        self.treeview.heading("Username", text="Username")
        self.treeview.heading("First Name", text="First Name")
        self.treeview.heading("Last Name", text="Last Name")
        self.treeview.heading("Initial Amount", text="Initial Amount")
        self.treeview.pack()

    def create_form(self):
        form_frame = ttk.Frame(self.window, style="Custom.TFrame")
        form_frame.pack()
        style = ttk.Style()

        style.configure("AddButton.TButton", background="#4CAF50")
        style.configure("UpdateButton.TButton", background="#2196F3")
        style.configure("DeleteButton.TButton", background="#F44336")
        style.configure("TButton", background="#FF9800")

        username_label = ttk.Label(form_frame, text="Username:")
        username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        password_label = ttk.Label(form_frame, text="Password:")
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        first_name_label = ttk.Label(form_frame, text="First Name:")
        first_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        last_name_label = ttk.Label(form_frame, text="Last Name:")
        last_name_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        initial_amount_label = ttk.Label(form_frame, text="Initial Amount:")
        initial_amount_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.password_entry = ttk.Entry(form_frame)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.first_name_entry = ttk.Entry(form_frame)
        self.first_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.last_name_entry = ttk.Entry(form_frame)
        self.last_name_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.initial_amount_entry = ttk.Entry(form_frame)
        self.initial_amount_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        add_button = ttk.Button(form_frame, text="Add", command=self.add_entry, style="AddButton.TButton")
        add_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        update_button = ttk.Button(form_frame, text="Update", command=self.edit_entry, style="UpdateButton.TButton")
        update_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")

        delete_button = ttk.Button(form_frame, text="Delete", command=self.delete_entry, style="DeleteButton.TButton")
        delete_button.grid(row=2, column=2, padx=5, pady=5, sticky="e")

        delete_all_button = ttk.Button(form_frame, text="Delete All Entries", command=self.delete_all_entries,
                                       style="DeleteButton.TButton")
        delete_all_button.grid(row=3, column=2, columnspan=3, padx=5, pady=10)

        logout_button = ttk.Button(self.window, text="Log Out", command=self.logout, style="TButton")
        logout_button.pack(side="bottom", pady=10)

        # Apply styling to buttons


    def populate_treeview(self):
        self.treeview.delete(*self.treeview.get_children())

        self.cursor.execute("SELECT * FROM tbl_login INNER JOIN tbl_account ON tbl_login.user_Id = tbl_account.user_Id")
        entries = self.cursor.fetchall()

        for entry in entries:
            user_id = entry[0]
            username = entry[1]
            first_name = entry[4]
            last_name = entry[5]
            initial_amount = entry[6]

            self.treeview.insert("", "end", text=user_id, values=(username, first_name, last_name, initial_amount))

    def populate_form(self, event):
        selected_item = self.treeview.selection()
        if not selected_item:
            return

        self.clear_form()

        user_id = self.treeview.item(selected_item)["text"]
        entry = self.get_entry_details(user_id)

        if entry:
            self.username_entry.insert(0, entry[1])
            self.password_entry.insert(0, entry[2])
            self.first_name_entry.insert(0, entry[4])
            self.last_name_entry.insert(0, entry[5])
            self.initial_amount_entry.insert(0, entry[6])

    def get_entry_details(self, user_id):
        self.cursor.execute(
            "SELECT * FROM tbl_login INNER JOIN tbl_account ON tbl_login.user_Id = tbl_account.user_Id WHERE tbl_login.user_Id = %s",
            (user_id,)
        )
        entry = self.cursor.fetchone()
        return entry

    def add_entry(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        initial_amount = self.initial_amount_entry.get()

        self.cursor.fetchall()

        self.cursor.execute("INSERT INTO tbl_login (username, password) VALUES (%s, %s)", (username, password))
        self.conn.commit()

        user_id = self.cursor.lastrowid

        self.cursor.fetchall()

        self.cursor.execute(
            "INSERT INTO tbl_account (user_Id, first_name, last_name, initial_amount) VALUES (%s, %s, %s, %s)",
            (user_id, first_name, last_name, initial_amount))

        self.conn.commit()
        self.populate_treeview()
        self.clear_form()

    def edit_entry(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            return

        username = self.username_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        initial_amount = self.initial_amount_entry.get()

        user_id = self.treeview.item(selected_item)["text"]

        self.cursor.execute("UPDATE tbl_login SET username = %s, password = %s WHERE user_Id = %s", (username, password, user_id))
        self.cursor.execute(
            "UPDATE tbl_account SET first_name = %s, last_name = %s, initial_amount = %s WHERE user_Id = %s",
            (first_name, last_name, initial_amount, user_id))

        self.conn.commit()
        self.populate_treeview()
        self.clear_form()

    def delete_entry(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            return

        user_id = self.treeview.item(selected_item)["text"]

        self.cursor.execute("DELETE FROM tbl_account WHERE user_Id = %s", (user_id,))
        self.cursor.execute("DELETE FROM tbl_login WHERE user_Id = %s", (user_id,))

        self.conn.commit()
        self.populate_treeview()
        self.clear_form()

    def delete_all_entries(self):
        confirmed = messagebox.askyesno("Delete All Entries",
                                        "Are you sure you want to delete all entries? This action cannot be undone.")
        if confirmed:
            self.cursor.execute("DELETE FROM tbl_account")
            self.cursor.execute("DELETE FROM tbl_login")
            self.conn.commit()
            self.populate_treeview()
            self.clear_form()

    def clear_form(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.first_name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.initial_amount_entry.delete(0, "end")

    def run(self):
        window_width = 600
        window_height = 600
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.mainloop()

    def logout(self):
        self.window.withdraw()
        login_window = tk.Tk()
        from LoginModule import LoginWindow
        login_module = LoginWindow(login_window)
        login_module.open_login_window()
        login_window.mainloop()


if __name__ == "__main__":
    window = tk.Tk()
    from LoginModule import LoginWindow
    admin_module = AdminModule(window)
    admin_module.run()
