
import sqlalchemy as sa
import sqlalchemy.orm as so

from shatelCore.model import BaseModel
from shatelCore.extensions import db


class NewsLetter(BaseModel):
    """newsletter model"""
    __tablename__ = BaseModel.SetTableName("news-letter")

    Email: so.Mapped[str] = so.mapped_column(sa.String(512), unique=True, nullable=False)

    # activation time is creation time

    def setEmail(self, email: str):
        if (db.session.execute(db.select(NewsLetter).filter_by(Email=email)).scalar_one_or_none()):
            return False
        self.Email = email
        return True

    @classmethod
    def is_subscribed(cls, email:str) -> bool:
        """this class method get an email address and check if its register in news letter or not"""
        query = db.session.select(cls).filter_by(Email=email)
        result = db.session.execute(query).scalar_one_or_none()
        return result



class ContactUs(BaseModel):
    """contact-us model"""
    __tablename__ = BaseModel.SetTableName("contact-us")

    Name: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True, nullable=False)
    Email: so.Mapped[str] = so.mapped_column(sa.String(512), unique=True, nullable=False)
    Title: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True, nullable=False)
    Message: so.Mapped[str] = so.mapped_column(sa.String(4096), unique=True, nullable=False)
    is_answered: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    admin_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey("Admin.id - replace "), nullable=True, unique=False)