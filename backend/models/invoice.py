from sqlalchemy import DateTime , Column , Integer , String ,  ForeignKey , Float
import datetime
from backend.database.test_db import base


class Invoice(base):
    __tablename__ = "invoices"

    invoice_id = Column(Integer , primary_key=True , index=True)
    customer_id = Column(Integer , ForeignKey("customers.customer_id"))
    invoice_date = Column(DateTime , default=datetime.datetime.utcnow)
    due_date = Column(DateTime , default=datetime.datetime.utcnow)
    status = Column(String , nullable=False)
    total_amount = Column(Float , nullable=False)
    payment_status = Column(String , nullable=False)
    created_at = Column(DateTime , default=datetime.datetime.utcnow)
    #updated_at if necessary

