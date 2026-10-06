import customtkinter as ctk

ACCENT = "#6C4CF1"


class DashboardFrame(ctk.CTkFrame):
    """Empty starter dashboard. Title and role text come from the user object (polymorphism)."""

    def __init__(self, master, app, user):
        super().__init__(master, fg_color="transparent")
        self._app = app

        header = ctk.CTkFrame(self, height=64, corner_radius=0, fg_color=ACCENT)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="EventAura", font=("Segoe UI", 22, "bold"), text_color="white").pack(
            side="left", padx=24
        )
        ctk.CTkButton(
            header, text="Log out", width=90, fg_color="white", text_color=ACCENT,
            hover_color="#EDE8FF", command=app.show_login,
        ).pack(side="right", padx=24)
        ctk.CTkLabel(
            header, text=f"{user.full_name}  ·  {user.role_label}", text_color="white", font=("Segoe UI", 13)
        ).pack(side="right", padx=10)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=30, pady=24)
        ctk.CTkLabel(body, text=user.dashboard_title, font=("Segoe UI", 26, "bold"), anchor="w").pack(fill="x")
        ctk.CTkLabel(
            body, text=f"Welcome, {user.full_name}!", font=("Segoe UI", 14), text_color="gray45", anchor="w"
        ).pack(fill="x")

        # intentionally empty: modules will be added here later
        ctk.CTkFrame(body, corner_radius=12, border_width=1, border_color="#E2E2EA", fg_color="transparent").pack(
            fill="both", expand=True, pady=(20, 0)
        )
