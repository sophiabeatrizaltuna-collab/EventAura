
import random
import time
import customtkinter as ctk
from tkinter import messagebox
from database import get_connection, hash_password


class ForgotPasswordPage(ctk.CTkFrame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
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

        title = ctk.CTkLabel(self.box, text="Forgot Password", font=("Arial", 24, "bold"))
        title.pack(padx=60, pady=(30, 5))
        note = ctk.CTkLabel(self.box, text="Enter your registered email.")
        note.pack(pady=(0, 15))

        self.email_entry = ctk.CTkEntry(self.box, placeholder_text="Email", width=280)
        self.email_entry.pack(pady=6)

        self.message_label = ctk.CTkLabel(self.box, text="", text_color="red")
        self.message_label.pack()

        send_button = ctk.CTkButton(self.box, text="Send Reset Code", width=280, command=self.send_code)
        send_button.pack(pady=(8, 4))
        back_button = ctk.CTkButton(self.box, text="Back to Login", width=280, command=self.window.show_login)
        back_button.pack(pady=(4, 30))

    def send_code(self):
        email = self.email_entry.get().strip().lower()
        if email == "":
            self.message_label.configure(text="Please enter your email.")
            return

        conn = get_connection()
        user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user is None:
            self.message_label.configure(text="Email not found.")
            return

        self.email = email
        self.make_code()
        self.show_step_two()

    def make_code(self):
        """Make a new 6-digit code and 'send' it."""
        self.code = str(random.randint(100000, 999999))
        self.code_time = time.time()
        messagebox.showinfo("Reset Code Sent",
                            "Reset code sent to " + self.email + "\n\n"
                            "(School project: no real email is sent.)\n"
                            "Your code is: " + self.code + "\n\nIt works for 10 minutes.")

    
    def show_step_two(self):
        self.clear_box()

        title = ctk.CTkLabel(self.box, text="Reset Password", font=("Arial", 24, "bold"))
        title.pack(padx=60, pady=(30, 5))
        note = ctk.CTkLabel(self.box, text="Enter the code, then your new password.")
        note.pack(pady=(0, 15))

        self.code_entry = ctk.CTkEntry(self.box, placeholder_text="6-digit code", width=280)
        self.code_entry.pack(pady=5)
        self.new_password_entry = ctk.CTkEntry(self.box, placeholder_text="New password (6+ characters)", show="*", width=280)
        self.new_password_entry.pack(pady=5)
        self.confirm_entry = ctk.CTkEntry(self.box, placeholder_text="Confirm new password", show="*", width=280)
        self.confirm_entry.pack(pady=5)

        self.message_label = ctk.CTkLabel(self.box, text="", text_color="red")
        self.message_label.pack()

        update_button = ctk.CTkButton(self.box, text="Update Password", width=280, command=self.update_password)
        update_button.pack(pady=(8, 4))
        resend_button = ctk.CTkButton(self.box, text="Resend Code", width=280, command=self.resend_code)
        resend_button.pack(pady=4)
        back_button = ctk.CTkButton(self.box, text="Back to Login", width=280, command=self.window.show_login)
        back_button.pack(pady=(4, 30))

    def resend_code(self):
        self.make_code()

    def update_password(self):
        code = self.code_entry.get().strip()
        new_password = self.new_password_entry.get()
        confirm = self.confirm_entry.get()

       
        if code != self.code:
            self.message_label.configure(text="Wrong code.")
            return
        if time.time() - self.code_time > 600:          # 600 seconds = 10 minutes
            self.message_label.configure(text="The code expired. Click Resend Code.")
            return

        
        if len(new_password) < 6:
            self.message_label.configure(text="Password must be at least 6 characters.")
            return
        if new_password != confirm:
            self.message_label.configure(text="The two passwords are not the same.")
            return

        
        conn = get_connection()
        conn.execute("UPDATE users SET password = ? WHERE email = ?", (hash_password(new_password), self.email))
        conn.commit()
        conn.close()

        self.code = None                
        messagebox.showinfo("EventAura", "Password updated. You can now log in.")
        self.window.show_login()
