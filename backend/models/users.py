from sqlalchemy import Column , String , PrimaryKeyConstraint , Integer , DateTime , Boolean
import datetime
from backend.database.test_db import base


class User(base):
    __tablename__ = "users"

    id = Column(Integer , primary_key=True , index = True)
    username = Column(String , nullable=False)
    email = Column(String , nullable=False , unique=True)
    password = Column(String , nullable=False)
    create_at = Column(DateTime , default=datetime.datetime.utcnow)
    verified = Column(Boolean , default = False)