import asyncio
from backend.database.test_db import base, engine
from backend.models.users import User  # ✅ IMPORT your User model

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
        print("Tables Created Successfully")

if __name__ == "__main__":
    asyncio.run(create_tables())
