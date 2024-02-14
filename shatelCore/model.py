import uuid
import datetime


from flask import current_app

from .extensions import db
from .utils import TimeStamp


from sqlalchemy import String, DateTime, Integer, Column
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

    id = Column(Integer, primary_key=True)

    @staticmethod
    def SetTableName(name):
        """Use This Method For setting a table name"""
        name = name.replace("-", "_").replace(" ", "")
        return f"{DATABASE_TABLE_PREFIX_NAME}{name}".lower()

    def SetPublicKey(self):
        """This Method Set a Unique PublicKey """
        while True:
            token = str(uuid.uuid4())
            if self.query.filter(self.PublicKey == token).first():
                continue
            else:
                self.PublicKey = token
                break

    def ConvertToJalali(self, t):
        timerConv = TimeStamp()
        jalali = timerConv.convert_grg2_jalali_dt(t)
        return str(jalali.date())


    def save(self, show_traceback:bool=False):
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



    PublicKey = Column(String(36), nullable=False, unique=True)
    CreatedTime = Column(DateTime, default=datetime.datetime.utcnow)
    LastUpdateTime = Column(DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)

