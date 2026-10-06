import customtkinter as ctk

from auth_service import AuthError

ACCENT = "#6C4CF1"


class SignupFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self._app = app

        card = ctk.CTkFrame(self, corner_radius=16, border_width=1, border_color="#E2E2EA")
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Create your account", font=("Segoe UI", 26, "bold"), text_color=ACCENT).pack(
            padx=50, pady=(30, 0)
        )
        ctk.CTkLabel(card, text="Join EventAura", font=("Segoe UI", 14), text_color="gray45").pack(pady=(0, 14))

        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(padx=40)
        form.grid_columnconfigure((0, 1), weight=1)

        self._name = self._field(form, 0, "Full name", 0, "Juan Dela Cruz")
        self._username = self._field(form, 0, "Username", 1, "juan_dc")
        self._email = self._field(form, 2, "Email", 0, "name@example.com", span=2)
        self._password = self._field(form, 4, "Password", 0, "Min. 8 chars, letter + number", secret=True)
        self._confirm = self._field(form, 4, "Confirm password", 1, "Re-enter password", secret=True)

        self._show = ctk.CTkCheckBox(form, text="Show passwords", command=self._toggle_password)
        self._show.grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 0), padx=4)

        ctk.CTkLabel(form, text="Account type", anchor="w").grid(row=7, column=0, columnspan=2, sticky="w", padx=4, pady=(10, 0))
        self._role = ctk.CTkSegmentedButton(
            form, values=["User", "Staff"], command=self._on_role_change, selected_color=ACCENT
        )
        self._role.set("User")
        self._role.grid(row=8, column=0, columnspan=2, sticky="ew", padx=4)

        # staff-only section (hidden until Staff is selected)
        self._staff_box = ctk.CTkFrame(form, fg_color="transparent")
        self._staff_box.grid(row=9, column=0, columnspan=2, sticky="ew")
        ctk.CTkLabel(
            self._staff_box, text="Staff credentials (staff ID, position, supervisor, etc.)", anchor="w"
        ).pack(fill="x", padx=4, pady=(10, 0))
        self._credentials = ctk.CTkTextbox(self._staff_box, height=70, border_width=1, border_color="#CFCFD8")
        self._credentials.pack(fill="x", padx=4)
        ctk.CTkLabel(
            self._staff_box, text="Staff accounts must be approved by an administrator before you can log in.",
            font=("Segoe UI", 11), text_color="gray45", wraplength=420, justify="left", anchor="w",
        ).pack(fill="x", padx=4, pady=(2, 0))
        self._staff_box.grid_remove()

        self._error = ctk.CTkLabel(card, text="", text_color="#D93025", wraplength=440, font=("Segoe UI", 12))
        self._error.pack(pady=(10, 0))

        ctk.CTkButton(card, text="Sign Up", width=440, height=40, fg_color=ACCENT, command=self._submit).pack(
            padx=40, pady=(6, 8)
        )

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(pady=(0, 24))
        ctk.CTkLabel(row, text="Already have an account?", text_color="gray45").pack(side="left")
        ctk.CTkButton(
            row, text="Log in", width=60, fg_color="transparent", text_color=ACCENT,
            hover_color="#F0ECFF", command=app.show_login,
        ).pack(side="left")

    @staticmethod
    def _field(parent, row, label, col, placeholder, span=1, secret=False):
        ctk.CTkLabel(parent, text=label, anchor="w").grid(
            row=row, column=col, columnspan=span, sticky="w", padx=4, pady=(8, 0)
        )
        entry = ctk.CTkEntry(
            parent, height=38, placeholder_text=placeholder, show="•" if secret else "", width=210 if span == 1 else 430
        )
        entry.grid(row=row + 1, column=col, columnspan=span, sticky="ew", padx=4)
        return entry

    def _toggle_password(self):
        show = "" if self._show.get() else "•"
        self._password.configure(show=show)
        self._confirm.configure(show=show)

    def _on_role_change(self, value):
        if value == "Staff":
            self._staff_box.grid()
        else:
            self._staff_box.grid_remove()

    def _submit(self):
        role = "staff" if self._role.get() == "Staff" else "user"
        try:
            status = self._app.auth.register(
                self._name.get(), self._username.get(), self._email.get(),
                self._password.get(), self._confirm.get(), role,
                self._credentials.get("1.0", "end"),
            )
        except AuthError as err:
            self._error.configure(text=str(err))
            return

        if status == "pending":
            msg = "Staff application submitted. You can log in once an administrator approves it."
        else:
            msg = "Account created! You can now log in."
        self._app.show_login(notice=msg)
