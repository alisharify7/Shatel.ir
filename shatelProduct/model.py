import enum
import json
from sqlalchemy import Column, String, JSON

from shatelCore.model import BaseModel
from shatelCore.extensions import db
#
# class Modem(BaseModel):
#     """Base Modem Table Model
#     """
#
#     class EnumType(enum.Enum):
#         """Enum Type for Modems
#         """
#         ADSLVDSL = "adsl-vdsl"
#         TDLTE = "tdlte"
#         FTTH = "ftth"
#
#     __tablename__ = BaseModel.SetTableName("models")
#     Name = Column(String(256), nullable=False, unique=True)
#     Caption = Column(String(2048), nullable=False, unique=True, index=True)
#     Type = Column(db.Enum(EnumType))
#     Feature = Column(JSON, nullable=False, unique=True, default=json.dumps({}))
#     Manual = Column(String(512), nullable=True, unique=True)
#
#
