from backend.models.otp import OTP
from backend.database.test_db import mysession
from sqlalchemy.future import select

async def store_otp(code : str , userId : int):
    async with mysession() as session:
        try:
            new_otp = OTP(
                user_id = userId,
                code = code
            )
            session.add(new_otp)
            await session.commit()
            await session.refresh(new_otp)
        except Exception as e:
            await session.rollback()
            print(e)
            return None