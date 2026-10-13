
import customtkinter as ctk
from database import get_connection, hash_password


class LoginPage(ctk.CTkFrame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window            

        box = ctk.CTkFrame(self)
        box.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(box, text="EventAura", font=("Arial", 28, "bold"))
        title.pack(padx=60, pady=(30, 5))
        subtitle = ctk.CTkLabel(box, text="Log in to continue")
        subtitle.pack(pady=(0, 15))

        self.email_entry = ctk.CTkEntry(box, placeholder_text="Email", width=280)
        self.email_entry.pack(pady=6)

        self.password_entry = ctk.CTkEntry(box, placeholder_text="Password", show="*", width=280)
        self.password_entry.pack(pady=6)

        self.message_label = ctk.CTkLabel(box, text="", text_color="red")
        self.message_label.pack()

        login_button = ctk.CTkButton(box, text="Log In", width=280, command=self.login)
        login_button.pack(pady=(8, 4))

        forgot_button = ctk.CTkButton(box, text="Forgot Password?", width=280, command=window.show_forgot_password)
        forgot_button.pack(pady=4)

        signup_button = ctk.CTkButton(box, text="Sign Up", width=280, command=window.show_signup)
        signup_button.pack(pady=(4, 30))

        forgot_button = ctk.CTkButton(
    box,
    text="Forgot Password?",
    width=280,
    fg_color="transparent",
    text_color="#6C4CF1",
    hover_color="#EEEEEE",
    command=window.show_forgot_password
)
forgot_button.pack(pady=(8, 4))

    def login(self):
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get()

        if email == "" or password == "":
            self.message_label.configure(text="Please enter your email and password.")
            return

        conn = get_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        # 3. check the email and password
        if user is None or user["password"] != hash_password(password):
            self.message_label.configure(text="Invalid email or password.")
            return

        if user["status"] == "pending":
            self.message_label.configure(text="Your staff application is still being verified.")
            return
        if user["status"] != "active":
            self.message_label.configure(text="This account is not active.")
            return

        self.window.show_dashboard(user)