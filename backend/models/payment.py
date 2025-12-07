from sqlalchemy import Column , Integer , ForeignKey , DateTime , Float , String
import datetime
from backend.database.test_db import base


class Payment(base):
    __tablename__ = "payments"

    payment_id = Column(Integer , primary_key=True , index=True)
    invoice_id = Column(Integer , ForeignKey("invoices.invoice_id"))
    payment_date = Column(DateTime , default=datetime.datetime.utcnow)
    payment_amount = Column(Float , nullable=False)
    payment_method = Column(String , nullable=False)
    payment_status = Column(String , nullable=False)
    transaction_id = Column(String )
    created_at = Column(DateTime , default=datetime.datetime.utcnow)