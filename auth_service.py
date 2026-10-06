"""Authentication logic: validation, password hashing, signup and login rules."""
import hashlib
import hmac
import os
import re
import sqlite3

from database import Database
from models import User

DEFAULT_ADMIN = {
    "full_name": "System Administrator",
    "username": "admin",
    "email": "admin@eventaura.local",
    "password": "Admin@123",  # change after first login once that feature exists
}


class AuthError(Exception):
    """Raised for any validation or login failure; message is safe to show the user."""


class PasswordHasher:
    ITERATIONS = 200_000

    @classmethod
    def hash(cls, password):
        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, cls.ITERATIONS)
        return f"{cls.ITERATIONS}${salt.hex()}${digest.hex()}"

    @classmethod
    def verify(cls, password, stored):
        try:
            iterations, salt_hex, digest_hex = stored.split("$")
            digest = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
            )
            return hmac.compare_digest(digest.hex(), digest_hex)
        except (ValueError, AttributeError):
            return False


class Validator:
    USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{4,20}$")
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    @classmethod
    def check_signup(cls, full_name, username, email, password, confirm, role, credentials):
        if len(full_name) < 2:
            raise AuthError("Please enter your full name.")
        if not cls.USERNAME_RE.match(username):
            raise AuthError("Username must be 4-20 characters: letters, numbers or underscore.")
        if not cls.EMAIL_RE.match(email):
            raise AuthError("Please enter a valid email address.")
        if len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise AuthError("Password must be at least 8 characters with a letter and a number.")
        if password != confirm:
            raise AuthError("Passwords do not match.")
        if role == "staff" and len(credentials) < 10:
            raise AuthError("Staff accounts need credentials (e.g. staff ID, position, supervisor) for approval.")


class AuthService:
    def __init__(self, db: Database):
        self._db = db
        self._ensure_default_admin()

    def _ensure_default_admin(self):
        if self._db.count_role("admin") == 0:
            a = DEFAULT_ADMIN
            self._db.insert_user(
                a["full_name"], a["username"], a["email"], PasswordHasher.hash(a["password"]), "admin", "active"
            )

    def register(self, full_name, username, email, password, confirm, role, credentials=""):
        """Create an account. Returns the resulting status: 'active' or 'pending'."""
        full_name, username, email = full_name.strip(), username.strip(), email.strip()
        credentials = credentials.strip()
        if role not in ("user", "staff"):
            raise AuthError("Invalid account type.")
        Validator.check_signup(full_name, username, email, password, confirm, role, credentials)
        if self._db.username_exists(username):
            raise AuthError("That username is already taken.")
        if self._db.email_exists(email):
            raise AuthError("That email is already registered.")

        status = "pending" if role == "staff" else "active"
        try:
            self._db.insert_user(
                full_name, username, email, PasswordHasher.hash(password), role, status,
                credentials if role == "staff" else None,
            )
        except sqlite3.IntegrityError:
            raise AuthError("That username or email is already registered.")
        return status

    def login(self, identifier, password):
        identifier = identifier.strip()
        if not identifier or not password:
            raise AuthError("Please enter your username/email and password.")
        row = self._db.find_by_login(identifier)
        # same message for unknown user and wrong password (no account enumeration)
        if row is None or not PasswordHasher.verify(password, row["password_hash"]):
            raise AuthError("Invalid username/email or password.")

        status = row["status"]
        if status == "pending":
            raise AuthError("Your staff account is still waiting for administrator approval.")
        if status == "rejected":
            raise AuthError("Your staff application was not approved. Please contact an administrator.")
        if status == "deactivated":
            raise AuthError("This account has been deactivated. Please contact an administrator.")
        return User.from_row(row)
