# signup.py
# The Sign Up page.

import customtkinter as ctk
from tkinter import messagebox
from database import get_connection, hash_password


class SignupPage(ctk.CTkFrame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

        box = ctk.CTkFrame(self)
        box.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(box, text="Create an Account", font=("Arial", 24, "bold"))
        title.pack(padx=60, pady=(30, 15))

        self.name_entry = ctk.CTkEntry(box, placeholder_text="Full name", width=280)
        self.name_entry.pack(pady=5)

        self.email_entry = ctk.CTkEntry(box, placeholder_text="Email", width=280)
        self.email_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(box, placeholder_text="Password (6+ characters)", show="*", width=280)
        self.password_entry.pack(pady=5)

        # choose User or Staff
        self.type_buttons = ctk.CTkSegmentedButton(box, values=["User", "Staff"])
        self.type_buttons.set("User")
        self.type_buttons.pack(pady=8)

        note = ctk.CTkLabel(box, text="Staff accounts must be approved by an admin first.", text_color="gray")
        note.pack()

        self.message_label = ctk.CTkLabel(box, text="", text_color="red")
        self.message_label.pack()

        signup_button = ctk.CTkButton(box, text="Sign Up", width=280, command=self.signup)
        signup_button.pack(pady=(8, 4))

        back_button = ctk.CTkButton(box, text="Back to Login", width=280, command=window.show_login)
        back_button.pack(pady=(4, 30))

    def signup(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get()
        account_type = self.type_buttons.get()

        # check the inputs
        if len(name) < 2:
            self.message_label.configure(text="Please enter your full name.")
            return
        if "@" not in email or "." not in email:
            self.message_label.configure(text="Please enter a valid email.")
            return
        if len(password) < 6:
            self.message_label.configure(text="Password must be at least 6 characters.")
            return

        # users can log in right away, staff must wait for the admin
        if account_type == "Staff":
            role = "staff"
            status = "pending"
        else:
            role = "user"
            status = "active"

        conn = get_connection()

        # make sure the email is not used yet
        old = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if old is not None:
            conn.close()
            self.message_label.configure(text="That email is already registered.")
            return

        conn.execute(
            "INSERT INTO users (full_name, email, password, role, status) VALUES (?, ?, ?, ?, ?)",
            (name, email, hash_password(password), role, status))
        conn.commit()
        conn.close()

        if status == "pending":
            messagebox.showinfo("EventAura", "Application sent. Please wait for the admin to approve it.")
        else:
            messagebox.showinfo("EventAura", "Account created. You can now log in.")
        self.window.show_login()
