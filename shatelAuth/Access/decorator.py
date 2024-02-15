# build in
from functools import wraps

# framework
from flask import session, request, redirect, url_for, flash, abort
# lib
from flask_babel import lazy_gettext as _l

# app
from shatelAuth.model import User
from shatelCore.extensions import db


# TODO: remote this decorator and use login_manager decorator
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
            return redirect(url_for("auth.login_get", next=next))

        if not user.Active:
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        return f(*args, **kwargs)

    return inner


def only_reset_password(f):
    """Only reset password users """

    @wraps(f)
    def inner(*args, **kwargs):

        if not session.get("mail", False):
            abort(404)

        # get user id
        if not session.get("allow-set-password"):
            abort(404)

        return f(*args, **kwargs)

    return inner


def login_manager_required(roles: int = []):
    """
    Login Manager decorator

    use this decorator for generating new decorators base on permission id

        example:
            user permission id : 1
            user_login_required = login_manager_required(roles=[1])

            @app.route("/")
            @user_login_required()
            def view():
                ...
    """
    if not roles or len(roles) == 0:
        raise ValueError("empty role set is given")

    def login_required(f):
        """Base Login required Decorator for users"""

        @wraps(f)
        def inner(*args, **kwargs):

            next = request.url_rule
            message = "برای دسترسی به صفحه مورد نیاز ابتدا وارد حساب کاربری خود شوید"

            nonlocal roles
            if not roles or len(roles) == 0:
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            # check user login
            if not session.get("is-login", False):
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            # get user id
            if not session.get("account-id"):
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            # check user id
            try:
                user = db.session.get(User, session.get("account-id"))
                if not user:
                    raise ValueError
            except Exception as e:
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            # check password is same (not changed)
            # session stored hashed password not plain text :
            if user.Password != (session.get("password")):
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            if not user.Active:
                flash(message, "danger")
                return redirect(url_for("auth.login_get", next=next))

            return f(*args, **kwargs)

        return inner

    return login_required
