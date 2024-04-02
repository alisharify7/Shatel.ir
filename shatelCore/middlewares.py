from .extensions import db
from .utils import userLocalSelector

from flask import Blueprint,request, session, redirect, url_for, flash

from shatelAuth.model import User
from shatelConfig import Setting
from flask_babel import lazy_gettext as _l

blp = Blueprint('middlewares', __name__)



@blp.before_app_request
def set_user_statue():
    """
    Set Some Useful utils on request before heads up to view

    properties:

        0.0 request.user_object
            this prob return Users Object:<Sqlalchemy Object> from database if user is authenticated!
            first user is_authenticated to ensure that user is logged in then
            get user object from db

        0.1 request.current_language
            this prob return user current language:<str> < this prob uses local_selector flask_babel >

        0.2 request.is_authenticated
            this prob return user is authenticated: <bool> or nor


    """
    request.current_language = userLocalSelector()
    request.is_authenticated = session.get("login", False)
    request.user_object = db.session.execute(
        db.select(User).filter_by(id=session.get("account-id", None))).scalar_one_or_none()
    request.real_ip = request.headers.get('X-Real-Ip', request.remote_addr)


@blp.route("/lang/set/<string:language>/", methods=["GET"])
def setUserLanguage(language):
    """
        this view select a  language for user
    """
    location = (request.referrer or url_for('web.index_get'))
    if language not in Setting.LANGUAGES:
        return redirect(location)
    else:
        flash(_l('زبان با موفقیت تغییر کرد'), "success")
        session["language"] = language
        return redirect(location)

