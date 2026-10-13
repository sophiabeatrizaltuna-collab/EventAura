# main.py
# Run this file to start the program:   python main.py
# It creates the window and decides which page to show.

import customtkinter as ctk
from database import create_tables, add_starting_data
from login import LoginPage
from signup import SignupPage
from forgot_password import ForgotPasswordPage
from user_dashboard import UserDashboard
from staff_dashboard import StaffDashboard
from admin_dashboard import AdminDashboard


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EventAura")
        self.geometry("1000x620")
        self.minsize(900, 560)
        self.current_page = None
        self.show_login()               # the first page is the login page

    def show_page(self, page):
        """Remove the old page and show the new one."""
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = page
        self.current_page.pack(fill="both", expand=True)

    def show_login(self):
        self.show_page(LoginPage(self))

    def show_signup(self):
        self.show_page(SignupPage(self))

    def show_forgot_password(self):
        self.show_page(ForgotPasswordPage(self))

    def show_dashboard(self, user):
        # each role has its own dashboard
        if user["role"] == "admin":
            self.show_page(AdminDashboard(self, user))
        elif user["role"] == "staff":
            self.show_page(StaffDashboard(self, user))
        else:
            self.show_page(UserDashboard(self, user))


# this part runs when you start the file
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    create_tables()
    add_starting_data()
    app = App()
    app.mainloop()