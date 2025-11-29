from sqlalchemy import Column , Integer , String , DateTime , ForeignKey , PrimaryKeyConstraint
from backend.database.test_db import base
import datetime


class OTP(base):
    __tablename__ = "otp"

    id = Column(Integer , primary_key=True , index=True)
    user_id = Column(Integer , ForeignKey("users.id"))
    code = Column(String , nullable = False)
    created_at = Column(DateTime , default = datetime.datetime.utcnow)
    expire_at = Column(DateTime , default = lambda : datetime.datetime.utcnow() + (datetime.timedelta(minutes=5)))