"""Domain models. Abstract User with Client / Staff / Administrator subclasses."""
from abc import ABC, abstractmethod


class User(ABC):
    ROLE = ""

    def __init__(self, user_id, full_name, username, email, status):
        self._id = user_id
        self._full_name = full_name
        self._username = username
        self._email = email
        self._status = status

    # encapsulation: read-only access
    @property
    def id(self):
        return self._id

    @property
    def full_name(self):
        return self._full_name

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def status(self):
        return self._status

    @property
    def role(self):
        return self.ROLE

    # polymorphism: each role supplies its own dashboard text
    @property
    @abstractmethod
    def dashboard_title(self):
        ...

    @property
    @abstractmethod
    def role_label(self):
        ...

    @staticmethod
    def from_row(row):
        """Factory: build the right subclass from a database row."""
        classes = {"user": Client, "staff": Staff, "admin": Administrator}
        cls = classes[row["role"]]
        return cls(row["id"], row["full_name"], row["username"], row["email"], row["status"])


class Client(User):
    ROLE = "user"
    dashboard_title = "User Dashboard"
    role_label = "Client"


class Staff(User):
    ROLE = "staff"
    dashboard_title = "Staff Dashboard"
    role_label = "Staff"


class Administrator(User):
    ROLE = "admin"
    dashboard_title = "Admin Dashboard"
    role_label = "Administrator"
