import asyncio
from backend.database.test_db import base, engine
from backend.models.users import User 
from backend.models.otp import OTP
from backend.models.customers import Customer
from backend.models.invoice import Invoice
from backend.models.payment import Payment
from backend.models.products import Product
from backend.models.task import Task

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
        print("Tables Created Successfully")

if __name__ == "__main__":
    asyncio.run(create_tables())
