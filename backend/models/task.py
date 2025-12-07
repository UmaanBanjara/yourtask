from sqlalchemy import Column , Integer , String , DateTime , ForeignKey  , Text
import datetime
from backend.database.test_db import base


class Task(base):
    __tablename__ = "tasks"

    task_id = Column(Integer , primary_key=True , index=True)
    customer_id = Column(Integer , ForeignKey("customers.customer_id"))
    task_description = Column(Text , nullable=False)
    status = Column(String , nullable=False)
    due_date = Column(DateTime , default=datetime.datetime.utcnow)
    priority = Column(String , nullable=False)
    created_at = Column(DateTime , default=datetime.datetime.utcnow)
    #updated_at if necessar