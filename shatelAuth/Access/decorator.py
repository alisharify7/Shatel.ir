from functools import wraps

from flask import session, request, redirect, url_for, flash, abort

from shatelAuth.model import User
from shatelAdmin.model import Admin

from flask_babel import lazy_gettext as _l


def login_required(f):
    """Base Login required Decorator for users"""

    @wraps(f)
    def inner(*args, **kwargs):
        next = request.url_rule

        # check user login
        message = _l("برای دسترسی به صفحه مورد نیاز ابتدا وارد حساب کاربری خود شوید")
        if not session.get("login", False):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # get user id
        if not session.get("account-id"):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # check user id
        try:
            user = User.query.get(session.get("account-id"))
            if not user:
                raise ValueError
        except Exception as e:
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # check password
        if user.Password != (session.get("password")):
            flash(message, "danger")
            print("herwe")
            return redirect(url_for("auth.login_get", next=next))

        if not user.Active:
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        return f(*args, **kwargs)

    return inner


def only_reset_password(f):
    """"""

    @wraps(f)
    def inner(*args, **kwargs):

        if not session.get("mail", False):
            return redirect(url_for("auth.login_get"))

        # get user id
        if not session.get("allow-set-password"):
            return redirect(url_for("auth.login_get"))

        return f(*args, **kwargs)

    return inner


def admin_login_required(f, Roles: list):
    """
    This Function Take a Role and return a Custom decorator Access Control for That Role

        >> return_a_decorator = create_custom_login_decorator(RoleName="admin")

        @app.get("url")
        @return_a_decorator
        def view_func():
            pass

        # doc Num : page 64 - 80
    """

    @wraps(f)
    def inner(*args, **kwargs):
        if not (user_id := session.get("account-id")):
            session.clear()
            abort(401)

        return f(*args, **kwargs)

    return inner
