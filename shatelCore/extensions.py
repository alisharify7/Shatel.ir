# flask extensions

from flask_babel import Babel
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from shatelConfig import Setting

RedisServer = Setting.REDIS_DEFAULT_INTERFACE

db = SQLAlchemy()
babel = Babel()
csrf = CSRFProtect()
ServerSession = Session()
ServerMigrate = Migrate()
ServerMail = Mail()
