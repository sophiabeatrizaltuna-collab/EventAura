import customtkinter as ctk

from gui.dashboard import DashboardFrame
from gui.login import LoginFrame
from gui.signup import SignupFrame

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class EventAuraApp(ctk.CTk):
    """Main window. Swaps one full-window frame at a time."""

    def __init__(self, auth):
        super().__init__()
        self.auth = auth
        self.title("EventAura")
        self.geometry("1000x760")
        self.minsize(900, 700)
        self._current = None
        self.show_login()

    def _swap(self, frame):
        if self._current is not None:
            self._current.destroy()
        self._current = frame
        frame.pack(fill="both", expand=True)

    def show_login(self, notice=None):
        self._swap(LoginFrame(self, self, notice))

    def show_signup(self):
        self._swap(SignupFrame(self, self))

    def show_dashboard(self, user):
        self._swap(DashboardFrame(self, self, user))
