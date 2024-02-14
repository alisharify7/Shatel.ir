from shatelCore.model import BaseModel
from shatelCore.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    """
        Users Model Table
    """
    __tablename__ = BaseModel.SetTableName("users")
    FirstName = Column(String(256), nullable=True, unique=False)
    LastName = Column(String(256), nullable=True, unique=False)

    Username = Column(String(128), nullable=False, unique=True)
    Password = Column(String(162), nullable=False, unique=True)
    Email = Column(String(256), nullable=False, unique=True)

    Address = Column(String(2048), nullable=True, unique=False)
    PhoneNumber = Column(String(14), nullable=True, unique=True)

    Active = Column(Boolean, default=False, nullable=False, unique=False)

    Tickets = db.relationship("Ticket", backref="User", lazy="dynamic")

    def getName(self, unique=False):
        """This Method Return Users Full name <f,l>"""
        if unique:
            return f"{self.FirstName} {self.LastName} - {self.PublicKey}"

        return f"{self.FirstName} {self.LastName}"

    def setPassword(self, password: str) -> None:
        self.Password = generate_password_hash(password)

    def checkPassword(self, password: str) -> bool:
        return check_password_hash(pwhash=self.Password, password=password)

    def setUsername(self, username: str) -> bool:
        print(self.query.filter_by(Username=username).first(), "old")
        print(db.session.execute(db.select(User).filter_by(Username=username)).scalar_one_or_none(), "new")
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
    Title = Column(String(64), nullable=False, unique=False)
    Caption = Column(String(512), nullable=False, unique=False)
    Status = Column(Boolean, default=False)

    UserID = Column(Integer, ForeignKey(BaseModel.SetTableName("users") + ".id"), nullable=False, unique=False)
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
    Message = Column(String(512), nullable=False, unique=False)

    AdminID = Column(Integer, ForeignKey(BaseModel.SetTableName("admins") + ".id"), nullable=False, unique=False)
    TicketID = Column(Integer, ForeignKey(BaseModel.SetTableName("tickets") + ".id"), nullable=True, unique=False)

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
