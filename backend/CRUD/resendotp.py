import random
import string
from backend.database.test_db import mysession
from backend.models.otp import OTP
from sqlalchemy import update
from sqlalchemy.future import select
from backend.utils.smtp import send_mail
import datetime
from datetime import timedelta


async def resend_otp(email: str, userId: int):
    async with mysession() as session:
        try:
            new_otp = "".join(random.choices(string.ascii_letters + string.digits, k=8))

            # Correct await usage
            res = await session.execute(select(OTP).filter_by(user_id=userId))
            result = res.scalar_one_or_none()

            if not result:
                return {'message': 'User doesnt exist'}

            await session.execute(update(OTP).where(OTP.user_id == userId).values(code=new_otp , created_at = datetime.datetime.utcnow() , expire_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)))
            await session.commit()

            await send_mail(
                subject='Verify your account',
                body=f"Your new OTP is {new_otp}",
                to=[email]
            )

            return {'message': 'OTP resend successfully'}

        except Exception as e:
            await session.rollback()
            print(e)
            return {'message': 'Something went wrong'}
