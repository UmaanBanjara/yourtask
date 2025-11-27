from backend.models.users import User
from backend.utils.pass_hash import verify_pass
from sqlalchemy.future import select
from backend.database.test_db import mysession
from backend.utils.jwt import create_access_token

#function to verify user
async def verify_user(email : str , password : str):
    async with mysession() as session:
        try:
            result = await session.execute(select(User).filter_by(email = email))
            user = result.scalar_one_or_none()

            if user is None:
                return {
                    'message' : "This User doesn't exits"
                }
            if verify_pass(password , user.password):
                token = create_access_token(data = {'id' : user.id})
                return {
                    'message' : 'Login Successfull',
                    'access_token' : token
                }
            else : 
                return {
                    'message' : 'The entered password is incorrect'
                }
        except Exception as e:
            return {
                'message' : 'Something went wrong. Please try again'
            }
       