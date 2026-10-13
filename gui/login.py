
import customtkinter as ctk
from database import Database
from auth_service import AuthService, AuthError


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

    def login(self):
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get()

        if not email or not password:
            self.message_label.configure(
                text="Please enter your email and password."
            )
            return

        from database import Database
        from auth_service import AuthService, AuthError

        try:
            auth = AuthService(Database())
            user = auth.login(email, password)

            self.window.show_dashboard(user)

        except AuthError as e:
            self.message_label.configure(text=str(e))

        except Exception as e:
            self.message_label.configure(
                text="Login failed. Please try again."
            )
            print("Login error:", e)
