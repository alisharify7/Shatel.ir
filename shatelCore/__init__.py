from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from shatelConfig import Setting

from .extensions import db, ServerSession, \
    ServerMigrate, ServerMail, babel, csrf

from .utils import celery_init_app, userLocalSelector

from flask_captcha2 import FlaskCaptcha

def create_app():
    """
        Factory Function For creating FlaskApp
    """
    app = Flask(
        __name__,
        template_folder="templates",
    )
    app.config.from_object(Setting)

    # register extensions
    db.init_app(app=app)  # db
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

    # captcha
    # captcha config
    ServerCaptchaMaster = FlaskCaptcha(app=app)
    ServerCaptcha2 = ServerCaptchaMaster.getGoogleCaptcha2(name='g-captcha2', conf=Setting.GOOGLE_CAPTCHA_V2_CONF)
    ServerCaptcha3 = ServerCaptchaMaster.getGoogleCaptcha3(name='g-captcha3', conf=Setting.GOOGLE_CAPTCHA_V3_CONF)
    app.extensions['master-captcha'] = ServerCaptchaMaster
    app.extensions['captcha2'] = ServerCaptcha2
    app.extensions['captcha3'] = ServerCaptcha3

    # register apps:
    from .middlewares import blp
    app.register_blueprint(blp, url_prefix="/")

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

    from .context_processors import contexts
    app.context_processor(contexts)

    from .template_filters import template_filders
    for each in template_filders:
        app.add_template_filter(template_filders[each], name=each)


    app.wsgi_app = ProxyFix(  # tell flask in behind a reverse proxy
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    return app




app = create_app()


