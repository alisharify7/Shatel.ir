# flask extensions

from flask_mail import Mail
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_captcha2 import FlaskCaptcha2, FlaskCaptcha3
from flask_babel import Babel
from shatelConfig import Setting
from flask_wtf.csrf import CSRFProtect


RedisServer = Setting.REDIS_DEFAULT_INTERFACE

db = SQLAlchemy()
babel = Babel()
csrf = CSRFProtect()
ServerSession = Session()
ServerMigrate = Migrate()
ServerMail = Mail()
ServerCaptcha2 = FlaskCaptcha2()
# ServerCaptcha3 = FlaskCaptcha3()
