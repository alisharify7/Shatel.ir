import sqlalchemy as sa
import sqlalchemy.orm as so

from werkzeug.security import generate_password_hash, check_password_hash

from shatelCore.extensions import db
from shatelCore.model import BaseModel



class User(BaseModel):
    """
        Users Model Table
    """
    __tablename__ = BaseModel.SetTableName("users")
    FirstName: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True, unique=False)
    LastName: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True, unique=False)

    Username: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False, unique=True)
    Password: so.Mapped[str] = so.mapped_column(sa.String(162), nullable=False, unique=True)
    Email: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False, unique=True)

    Address: so.Mapped[str] = so.mapped_column(sa.String(2048), nullable=True, unique=False)
    PhoneNumber: so.Mapped[str] = so.mapped_column(sa.String(14), nullable=True, unique=True)

    Active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False, unique=False)


    Tickets = db.relationship("Ticket", backref="User", lazy="dynamic")

    def to_dict(self):
        return {
            "Username": self.Username,
            "FirstName": self.FirstName or "NULL",
            "LastName": self.LastName or "NULL",
            "Address": self.Address or "NULL",
            "Email": self.Email,
            "PublicKey": self.PublicKey,
            "Status": "Active" if self.Active else "inactive",
            "CreatedTime": self.CreatedTime
        }

    def getName(self, unique=False):
        """This Method Return Users Full name <f,l>"""
        if unique:
            return f"{self.FirstName} {self.LastName} - {self.PublicKey}"

        return f"{self.FirstName} {self.LastName}"

    def setPassword(self, password: str) -> None:
        self.Password = generate_password_hash(password, method="scrypt")

    def checkPassword(self, password: str) -> bool:
        return check_password_hash(pwhash=self.Password, password=password)

    def setUsername(self, username: str) -> bool:
        if db.session.execute(db.select(User).filter_by(Username=username)).scalar_one_or_none():
            return False
        else:
            self.Username = username
            return True

    def setPhonenumber(self, phone: str) -> bool:
        if db.session.execute(db.select(User).filter_by(PhoneNumber=phone)).scalar_one_or_none():
            return False
        else:
            self.PhoneNumber = phone
            return True

    def setEmail(self, email: str) -> bool:
        if db.session.execute(db.select(User).filter_by(Email=email)).scalar_one_or_none():
            return False
        else:
            self.Email = email
            return True

    def setActivate(self):
        self.Active = True


class Ticket(BaseModel):
    __tablename__ = BaseModel.SetTableName("tickets")
    Title: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False, unique=False)
    Caption: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=False, unique=False)
    Status: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    File: so.Mapped[str] = so.mapped_column(sa.String(1024), unique=True, nullable=True)

    UserID: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id), nullable=False, unique=False)
    Answer = db.relationship("AnswerTicket", backref="GetTicket", lazy=True)

    def setTitle(self, title: str) -> None:
        self.Title = title

    def setCaption(self, caption: str) -> None:
        self.Caption = caption

    def setUserID(self, user: User) -> None:
        self.UserID = user.id

    def setAnswerStatus(self) -> None:
        self.Status = True

    def getAnswer(self):
        return self.Answer or False


class AnswerTicket(BaseModel):
    __tablename__ = BaseModel.SetTableName("answer-tickets")
    Message: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=False, unique=False)

    AdminID: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(BaseModel.SetTableName("admins") + ".id"),
                                               nullable=False, unique=False)
    TicketID: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(BaseModel.SetTableName("tickets") + ".id"),
                                                nullable=True, unique=False)

    def setMessage(self, message: str) -> None:
        self.Message = message

    def setTicket(self, ticket: Ticket) -> None:
        """
        Set TicketID in Foreignkey Column
        ticket: Ticket class Model Instance
        """
        self.TicketID = ticket.id

    def setAdmin(self, admin) -> None:
        """
        Set AdminID in Foreignkey Column
        admin: Admin class Model Instance
        """
        self.AdminID = admin.id


class NewsLetter(BaseModel):
    __tablename__ = BaseModel.SetTableName("news-letters")
    Email: so.Mapped[str] = so.mapped_column(sa.String(1024), nullable=False, unique=True)
    VerifiedAT: so.Mapped[str] = so.mapped_column(sa.DateTime, nullable=False, unique=False)