import uuid
import datetime
from typing import Optional

from flask import current_app
import sqlalchemy as sa
import sqlalchemy.orm as so

from .extensions import db
from .utils import TimeStamp

from shatelConfig.settings import DATABASE_TABLE_PREFIX_NAME



class BaseModel(db.Model):
    """
    Base model class for all models
     ~~~~~~~~~~~~~~ abstract model ~~~~~~~~~~~~~~~

    """
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_persian_ci'
    }

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    T = TimeStamp()

    @staticmethod
    def SetTableName(name):
        """Use This Method For setting a table name"""
        name = name.replace("-", "_").replace(" ", "")
        return f"{DATABASE_TABLE_PREFIX_NAME}{name}".lower()

    def SetPublicKey(self):
        """ This Method Set a Unique PublicKey """
        while True:
            token = uuid.uuid4().hex
            if self.query.filter(self.PublicKey == token).first():
                continue
            else:
                self.PublicKey = token
                break

    def ConvertToJalali(self, obj_time, full_time=False) -> str:
        """Convert to jalali time method """
        jalali = BaseModel.T.convert_grg2_jalali_dt(obj_time)
        if full_time:
            return str(jalali.date()) + "-" + str(jalali.time())
        else:
            return str(jalali.strftime("%D %B %Y"))

    def save(self, show_traceback: bool = True):
        """
         combination of two steps, add and commit session
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            if show_traceback:
                current_app.logger.exception(exc_info=e, msg=e)
            return False
        else:
            return True

    PublicKey: so.Mapped[str] = so.mapped_column(sa.String(36), nullable=False, unique=True)
    CreatedTime: so.Mapped[Optional[datetime.datetime]] = so.mapped_column(sa.DateTime,
                                                                           default=datetime.datetime.utcnow)
    LastUpdateTime: so.Mapped[Optional[datetime.datetime]] = so.mapped_column(sa.DateTime,
                                                                              onupdate=datetime.datetime.utcnow,
                                                                              default=datetime.datetime.utcnow)