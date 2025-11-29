from backend.database.test_db import mysession
from backend.models.otp import OTP
from sqlalchemy.future import select
from sqlalchemy import update
import datetime
from backend.models.users import User


async def verify_otp(code: str, userId: int):
    async with mysession() as session:
        try:
            verify_otp = await session.execute(
                select(OTP).filter_by(user_id=userId, code=code)
            )
            result = verify_otp.scalar_one_or_none()

            if not result:
                return {
                    'message': 'Invalid OTP'
                }

            if result.expire_at < datetime.datetime.utcnow():
                return {
                    'message': 'OTP Expired'
                }
            await session.execute(update(User).where(User.id == userId).values(verified = True)) #update the verified colum
            await session.commit()
            
            return {
                'message' : 'OTP verified successfully',
            }
            

        except Exception as e:
            print(e)
            return {
                'message': 'Something went wrong. Please try again'
            }
