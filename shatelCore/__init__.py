from flask import Flask, request, session, redirect, url_for
from shatelConfig import Setting
from .extensions import db, ServerCaptcha2, ServerSession, \
    ServerMigrate, ServerMail, babel, csrf
from .utils import celery_init_app, add_watermark
from shatelAuth.model import User

# cli
from .cli.make import MakeCommands
from shatelAdmin.cli.admin import AdminCommands


def create_app():
    """
        Factory Function For creating FlaskApp

     first we should update app config for extension configs
    """
    app = Flask(
        __name__,
        template_folder="MailTemplate",
    )
    app.config.from_object(Setting)

    # register extensions
    db.init_app(app=app)  # db
    ServerCaptcha2.init_app(app=app)  # captcha2
    csrf.init_app(app=app)
    ServerMail.init_app(app=app)  # mail
    ServerMigrate.init_app(db=extensions.db, app=app)  # migrate
    ServerSession.init_app(app=app)  # session
    babel.init_app(  # babel
        app=app,
        locale_selector=userLocalSelector,
        default_translation_directories=str((Setting.BASE_DIR / "translations").absolute())
    )

    celery = celery_init_app(app=app)  # celery

    # register apps:
    from shatelWeb import web
    app.register_blueprint(web, url_prefix="/")

    from shatelAdmin import admin
    app.register_blueprint(admin, url_prefix="/admin/")

    from shatelAuth import auth
    app.register_blueprint(auth, url_prefix="/auth/")

    from shatelUser import user
    app.register_blueprint(user, url_prefix="/user/")

    from shatelProduct import product
    app.register_blueprint(product, url_prefix="/product/")

    return app


def userLocalSelector():
    """
        this function select user local base on session
    """
    try:
        return session.get("language", "fa")
    except:
        return "en"


app = create_app()
app.cli.add_command(cmd=MakeCommands)
app.cli.add_command(cmd=AdminCommands)


@app.before_request
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


@app.route("/lang/set/<string:language>")
def setUserLanguage(language):
    """
        this view select a  language for user
    """
    location = (request.referrer or url_for('web.index_get'))

    if language not in Setting.LANGUAGES:
        return redirect(location)
    else:
        session["language"] = language
        return redirect(location)




import shatelCore.template_filter
import shatelCore.app_contextprocessors
