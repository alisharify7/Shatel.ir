import datetime
import os
from pathlib import Path

import redis
from dotenv import load_dotenv

from .utils import generate_secret_key

load_dotenv()
DATABASE_TABLE_PREFIX_NAME = os.environ.get("DATABASE_TABLE_PREFIX_NAME", "")


class Setting:
    """ Flask configuration Class
        base Setting os.environ class for flask app
    """

    SECRET_KEY = os.environ.get("APP_SECRET_KEY", generate_secret_key())
    ADMIN_LOGIN_TOKEN = os.environ.get("ADMIN_LOGIN_TOKEN", "123654")

    APP_DEBUG_STATUS = os.environ.get("APP_DEBUG", "") == "True"
    DEBUG = APP_DEBUG_STATUS
    FLASK_DEBUG = APP_DEBUG_STATUS

    DOMAIN = os.environ.get("SERVER", "")
    SERVER = "127.0.0.1"

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    STORAGE_DIR = BASE_DIR.joinpath("Storage")

    IMAGE_EXT_SAVE = ['.png', '.jpg', '.jpeg']
    PRODUCT_IMAGE_STORAGE = STORAGE_DIR / "product" / "images"
    if not os.path.exists(PRODUCT_IMAGE_STORAGE):
        os.mkdir(PRODUCT_IMAGE_STORAGE)

    # Database Config
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "")
    DATABASE_PORT = os.environ.get("DATABASE_PORT", "")
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "")
    DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", "")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "")
    DATABASE_TABLE_PREFIX_NAME = DATABASE_TABLE_PREFIX_NAME
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis Config
    REDIS_DEFAULT_URL = os.environ.get("REDIS_DEFAULT_URI")
    REDIS_DEFAULT_INTERFACE = redis.Redis().from_url(REDIS_DEFAULT_URL)

    # session cookie setting
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = '_session_cookie_'
    SESSION_REDIS = redis.Redis.from_url(os.environ.get("REDIS_SESSION_URI")) if os.environ.get("REDIS_SESSION_URI",
                                                                                                None) else REDIS_DEFAULT_INTERFACE

    # Recaptcha Config <Flask-captcha2>
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", '')
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", '')
    RECAPTCHA_ENABLED = os.environ.get("RECAPTCHA_ENABLED", False) == "True"
    RECAPTCHA_LOG = os.environ.get("RECAPTCHA_LOG", True) == "True"

    # RECAPTCHA_THEME = ''
    # RECAPTCHA_TYPE = ''
    # RECAPTCHA_SIZE = ''
    # RECAPTCHA_LANGUAGE = ''
    # RECAPTCHA_TABINDEX = ''

    # available languages
    LANGUAGES = {
        'fa': "فارسی/Farsi",
        'en': "English/American English",
        'ar': "عربي/Arabic",
        'tr': "Turkish/Türkçe",
        'ru': "Russian/Россия",
        'zh': "Chinese/中国人",
    }

    # Mail config
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    MAIL_USE_SSL = False
    MAIL_DEBUG = os.environ.get("MAIL_DEBUG") == "True"
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    # CACHE_TYPE = "RedisCache"  # NullCache for disable Flask-Caching related os.environs
    CACHE_TYPE = os.environ.get("CACHE_TYPE", 'NullCache')
    CACHE_DEFAULT_TIMEOUT = ((60 * 60) * 12)
    CACHE_REDIS_URL = os.environ.get("REDIS_CACHE_URI", REDIS_DEFAULT_URL)

    # celery config
    CELERY = dict(
        broker_url=os.environ.get("REDIS_CELERY_BROKER_URI", REDIS_DEFAULT_URL),
        result_backend=os.environ.get("REDIS_CELERY_BACKEND_URI", REDIS_DEFAULT_URL),
        broker_connection_retry_on_startup=True,
        result_serializer="pickle",
    )
