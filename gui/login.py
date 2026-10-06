import customtkinter as ctk

from auth_service import AuthError

ACCENT = "#6C4CF1"


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app, notice=None):
        super().__init__(master, fg_color="transparent")
        self._app = app

        card = ctk.CTkFrame(self, corner_radius=16, border_width=1, border_color="#E2E2EA")
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="EventAura", font=("Segoe UI", 30, "bold"), text_color=ACCENT).pack(
            padx=50, pady=(35, 0)
        )
        ctk.CTkLabel(card, text="Log in to continue", font=("Segoe UI", 14), text_color="gray45").pack(pady=(0, 20))

        self._notice = ctk.CTkLabel(card, text=notice or "", text_color="#1E8E3E", wraplength=320, font=("Segoe UI", 12))
        self._notice.pack()

        ctk.CTkLabel(card, text="Username or email", anchor="w").pack(fill="x", padx=50, pady=(6, 0))
        self._login = ctk.CTkEntry(card, width=320, height=38, placeholder_text="Enter username or email")
        self._login.pack(padx=50)

        ctk.CTkLabel(card, text="Password", anchor="w").pack(fill="x", padx=50, pady=(12, 0))
        self._password = ctk.CTkEntry(card, width=320, height=38, show="•", placeholder_text="Enter password")
        self._password.pack(padx=50)

        self._show = ctk.CTkCheckBox(card, text="Show password", command=self._toggle_password)
        self._show.pack(anchor="w", padx=50, pady=(10, 0))

        self._error = ctk.CTkLabel(card, text="", text_color="#D93025", wraplength=320, font=("Segoe UI", 12))
        self._error.pack(pady=(8, 0))

        ctk.CTkButton(card, text="Log In", width=320, height=40, fg_color=ACCENT, command=self._submit).pack(
            padx=50, pady=(6, 10)
        )

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(pady=(0, 30))
        ctk.CTkLabel(row, text="No account yet?", text_color="gray45").pack(side="left")
        ctk.CTkButton(
            row, text="Sign up", width=60, fg_color="transparent", text_color=ACCENT,
            hover_color="#F0ECFF", command=app.show_signup,
        ).pack(side="left")

        for entry in (self._login, self._password):
            entry.bind("<Return>", lambda _e: self._submit())
        self._login.focus()

    def _toggle_password(self):
        self._password.configure(show="" if self._show.get() else "•")

    def _submit(self):
        try:
            user = self._app.auth.login(self._login.get(), self._password.get())
        except AuthError as err:
            self._notice.configure(text="")
            self._error.configure(text=str(err))
            return
        self._app.show_dashboard(user)
