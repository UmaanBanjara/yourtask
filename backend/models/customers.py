from sqlalchemy import Integer , String , DateTime ,Column , Text
import datetime
from backend.database.test_db import base

class Customer(base):
    __tablename__ = "customers"

    customer_id = Column(Integer , primary_key=True , index=True)
    first_name = Column(String , nullable=False)
    last_name = Column(String , nullable=False)
    email = Column(String , nullable=False)
    phone_number = Column(String , nullable=False)
    address = Column(Text , nullable=False)
    city = Column(String , nullable=False)
    created_at = Column(DateTime , default=datetime.datetime.utcnow)
    #updated_at if necessary

