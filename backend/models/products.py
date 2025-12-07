from sqlalchemy import Column , Integer , String , Text , DateTime , Float
import datetime
from backend.database.test_db import base


class Product(base):
    __tablename__ = "products"

    product_id = Column(Integer , primary_key=True , index=True)
    name = Column(String , nullable=False)
    description = Column(Text , nullable=False)
    price = Column(Float , nullable=False)
    quantity_in_stock = Column(Integer , nullable=False)
    created_at = Column(DateTime , default=datetime.datetime.utcnow)
    #update_at if necessary