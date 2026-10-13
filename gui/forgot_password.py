
import random
import time
import customtkinter as ctk
from tkinter import messagebox

from auth_service import PasswordHasher
from database import Database


class ForgotPasswordPage(ctk.CTkFrame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window

        self.db = Database()
        self.email = ""
        self.code = None
        self.code_time = 0

        self.box = ctk.CTkFrame(self)
        self.box.place(relx=0.5, rely=0.5, anchor="center")

        self.show_step_one()

    def clear_box(self):
        for widget in self.box.winfo_children():
            widget.destroy()

    def show_step_one(self):
        self.clear_box()

        ctk.CTkLabel(
            self.box,
            text="Forgot Password",
            font=("Arial", 24, "bold")
        ).pack(padx=60, pady=(30, 5))

        ctk.CTkLabel(
            self.box,
            text="Enter your registered email."
        ).pack(pady=(0, 15))

        self.email_entry = ctk.CTkEntry(
            self.box, placeholder_text="Email", width=280
        )
        self.email_entry.pack(pady=6)

        self.message_label = ctk.CTkLabel(
            self.box, text="", text_color="red"
        )
        self.message_label.pack()

        ctk.CTkButton(
            self.box,
            text="Send Reset Code",
            width=280,
            command=self.send_code
        ).pack(pady=(8, 4))

        ctk.CTkButton(
            self.box,
            text="Back to Login",
            width=280,
            command=self.window.show_login
        ).pack(pady=(4, 30))

    def send_code(self):
        email = self.email_entry.get().strip().lower()

        if not email:
            self.message_label.configure(
                text="Please enter your email."
            )
            return

        user = self.db.find_by_email(email)

        if user is None:
            self.message_label.configure(
                text="Email not found."
            )
            return

        self.email = email
        self.make_code()
        self.show_step_two()

    def make_code(self):
        self.code = str(random.randint(100000, 999999))
        self.code_time = time.time()

        # Demo only: this displays the code instead of emailing it.
        messagebox.showinfo(
            "Reset Code",
            f"Your password reset code is: {self.code}\n\n"
            "This demo code expires in 10 minutes."
        )

    def show_step_two(self):
        self.clear_box()

        ctk.CTkLabel(
            self.box,
            text="Reset Password",
            font=("Arial", 24, "bold")
        ).pack(padx=60, pady=(30, 5))

        ctk.CTkLabel(
            self.box,
            text="Enter your code and new password."
        ).pack(pady=(0, 15))

        self.code_entry = ctk.CTkEntry(
            self.box, placeholder_text="6-digit code", width=280
        )
        self.code_entry.pack(pady=5)

        self.new_password_entry = ctk.CTkEntry(
            self.box,
            placeholder_text="New password (8+ characters)",
            show="*",
            width=280
        )
        self.new_password_entry.pack(pady=5)

        self.confirm_entry = ctk.CTkEntry(
            self.box,
            placeholder_text="Confirm new password",
            show="*",
            width=280
        )
        self.confirm_entry.pack(pady=5)

        self.message_label = ctk.CTkLabel(
            self.box, text="", text_color="red"
        )
        self.message_label.pack()

        ctk.CTkButton(
            self.box,
            text="Update Password",
            width=280,
            command=self.update_password
        ).pack(pady=(8, 4))

        ctk.CTkButton(
            self.box,
            text="Resend Code",
            width=280,
            command=self.resend_code
        ).pack(pady=4)

        ctk.CTkButton(
            self.box,
            text="Back to Login",
            width=280,
            command=self.window.show_login
        ).pack(pady=(4, 30))

    def resend_code(self):
        self.make_code()

    def update_password(self):
        code = self.code_entry.get().strip()
        new_password = self.new_password_entry.get()
        confirm = self.confirm_entry.get()

        if not self.code or code != self.code:
            self.message_label.configure(text="Wrong code.")
            return

        if time.time() - self.code_time > 600:
            self.message_label.configure(
                text="Code expired. Please request a new code."
            )
            return

        if (
            len(new_password) < 8
            or not any(c.isalpha() for c in new_password)
            or not any(c.isdigit() for c in new_password)
        ):
            self.message_label.configure(
                text="Use 8+ characters with a letter and a number."
            )
            return

        if new_password != confirm:
            self.message_label.configure(
                text="Passwords do not match."
            )
            return

        password_hash = PasswordHasher.hash(new_password)

        updated = self.db.update_password_hash(
            self.email, password_hash
        )

        if not updated:
            self.message_label.configure(
                text="Could not update the password. Please try again."
            )
            return

        self.code = None
        self.code_time = 0

        messagebox.showinfo(
            "EventAura",
            "Password updated successfully. You can now log in."
        )
        self.window.show_login()

