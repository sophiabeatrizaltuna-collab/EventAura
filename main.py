from auth_service import AuthService
from database import Database
from gui.app import EventAuraApp


def main():
    auth = AuthService(Database())
    EventAuraApp(auth).mainloop()


if __name__ == "__main__":
    main()
