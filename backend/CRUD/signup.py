from backend.models.users import User
from backend.utils.pass_hash import hash_pass
from backend.database.test_db import mysession
from sqlalchemy.future import select
from backend.models.otp import OTP
from backend.utils.smtp import send_mail
from backend.CRUD.otp import store_otp
import random
import string
from backend.tasks.customer_tasks import send_welcome_message


#function to create a new user
async def create_user (username : str , email : str , password : str):
    async with mysession() as session:
        try:
            result = await session.execute(select(User).filter_by(email=email))
            existing_user = result.scalar_one_or_none()
            if existing_user:
                return {
                    'message' : "User with this email already exits"
                }
            
            #hash password
            hashed_password = hash_pass(password)

            #new user
            new_user = User(username = username , email = email , password = hashed_password)

            #insert 
            session.add(new_user)

            #commit
            await session.commit()

            #refresh
            await session.refresh(new_user)

            #return info


            #generate otp
            new_otp = "".join(random.choices(string.ascii_letters + string.digits , k = 8))
            
            #store the otp
            await store_otp(
                userId=new_user.id,
                code = new_otp
            )

            await send_mail(
                body = f"Your Verification code is : {new_otp}",
                subject="Verify your account",
                to = [new_user.email]
            )

            send_welcome_message.apply_async(args = [new_user.id , new_user.email],countdown = 15* 60)

            return{
                'message' : 'User created successfully. OTP sent to your email',
                'userId' : new_user.id,
                'email' : new_user.email
            }
        
        except Exception as e:
            await session.rollback()
            print(e)
            return {
                'message' : 'Something went wrong please try again'
            }