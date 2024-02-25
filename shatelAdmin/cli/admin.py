import getpass
import re
import sys

from email_validator import validate_email
from flask.cli import AppGroup

from shatelAdmin.model import Admin, Permission

AdminCommands = AppGroup(name="admin", help="admin operation commands.")


@AdminCommands.command("create", help="create a new admin in database.")
def create_admin_account():
    """Create a new user with admin perivilagers"""
    def get_password():
        while True:
            password = getpass.getpass("Password: ")
            passwordConfirm = getpass.getpass("Password Confirm: ")

            if password != passwordConfirm:
                print("Passwords are not the same ...")
                continue
            else:
                return password

    def get_boolean(msg):
        while True:
            b = input(msg)
            try:
                return bool(b)
            except Exception as e:
                print(e)
                continue

    def get_input(msg):
        while True:
            m = input(msg)
            if not msg:
                continue
            return msg

    def get_email(msg):
        while True:
            email = input(msg)
            try:
                if validate_email(email):
                    return email
            except Exception as e:
                print("invalid email address ...")
                continue

    def get_phone_number(msg):
        while True:
            p = input(msg)
            if re.search(pattern=r"^((0|0098|\+98)?9\d{9})?$", string=p):
                return p
            continue

    username = get_input("Username:")

    password = get_password()
    email = get_email("Email: ")
    phone = get_phone_number("Phone number: ")
    active = get_boolean("Account Active: ")

    admin = Admin()
    if not admin.setUsername(username):
        print("duplicated Username ...")
        sys.exit()

    if not admin.setPhonenumber(phone):
        print("duplicated Phone number ...")
        sys.exit()

    admin.setPassword(password)
    admin.Active = active
