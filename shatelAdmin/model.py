from shatelCore.model import BaseModel
from shatelCore.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BIGINT, TEXT
from werkzeug.security import generate_password_hash, check_password_hash


AdminsPermission = db.Table(
    BaseModel.SetTableName("admins-permission"),
    Column("AdminID", ForeignKey(BaseModel.SetTableName("admins") + ".id")),
    Column("PermissionID", ForeignKey(BaseModel.SetTableName("permissions") + ".id"))
)


class Admin(BaseModel):
    __tablename__ = BaseModel.SetTableName("admins")

    Username = Column(String(256), unique=True, nullable=False)
    Password = Column(String(102), unique=False, nullable=False)
    Email = Column(String(512), unique=True, nullable=False)
    PhoneNumber = Column(String(14), unique=True, nullable=False)
    Active = Column(Boolean, default=False)
    TryNumber = Column(Integer, default=0)

    Permissions = db.relationship("Permission", secondary=AdminsPermission, backref="Admin", lazy="dynamic")

    def setPassword(self, password: str) -> None:
        self.Password = generate_password_hash(password)

    def checkPassword(self, password: str) -> bool:
        return check_password_hash(pwhash=self.Password, password=password)

    def setUsername(self, username: str) -> bool:
        if db.session.execute(db.select(self).filter_by(Username=username)).scalar_one_or_none():
            return False
        else:
            self.Username = username
            return True

    def setPhonenumber(self, phone: str) -> bool:
        if db.session.execute(db.select(self).filter_by(PhoneNumber=phone)).scalar_one_or_none():
            return False
        else:
            self.PhoneNumber = phone
            return True

    def setEmail(self, email: str) -> bool:
        if db.session.execute(db.select(self).filter_by(Email=email)).scalar_one_or_none():
            return False
        else:
            self.Email = email
            return True

    def setActivate(self):
        self.Active = True

    def allowToLogin(self):
        return False if self.TryNumber >= 5 else True

    def setLog(self, ip:str, action:str):
        log = AdminLog()
        log.SetIPaddress(ip)
        log.SetPublicKey()
        log.Action = action
        log.SetAdminID(self.id)
        return log.save()

    logs = db.relationship("AdminLog", backref='GetAdmin', lazy='dynamic')


class AdminLog(BaseModel):
    __tablename__ = BaseModel.SetTableName("admins-log-table")
    IP = Column(BIGINT, unique=False, nullable=False)
    AdminID = Column(Integer, ForeignKey(BaseModel.SetTableName("admins") + '.id'))
    Action = Column(TEXT, nullable=True, unique=False)

    def SetIPaddress(self, ip: str):
        """Set integer value of IP address"""
        import ipaddress
        try:
            ip = ipaddress.ip_address(ip)
            self.IP = int(ip)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def SetAdminID(self, admin_id: int):
        self.AdminID = admin_id


class Permission(BaseModel):
    """
     Permission Handler Table

        backref=GetAdmin
    """
    __tablename__ = BaseModel.SetTableName("permissions")
    Permission = Column(String(256), unique=True, nullable=False)
    Description = Column(String(1024), unique=False, nullable=False)

    default_permissions = [
        {"Permission": "manage-users", "Description": "add - update - delete - edit users"},
        {"Permission": "manage-tickets", "Description": "delete - view - and response tickets"},
        {"Permission": "manage-site-content", "Description": "manage products - manage index sliders news and ..."},
        {"Permission": "all", "Description": "manage products - manage index sliders news and ..."},
    ]
