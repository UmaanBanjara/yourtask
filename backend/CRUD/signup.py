from backend.models.users import User
from backend.utils.pass_hash import hash_pass
from backend.database.test_db import mysession
from sqlalchemy.future import select


#function to create a new user
async def create_user (username : str , email : str , password : str):
    async with mysession() as session:
        try:
            result = await session.execute(select(User).file(email=email))
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

            return {
                'message' : 'User create successfully',
                'user' : {
                    'id' : new_user.id,
                    'username' : new_user.username
                }
            }
        
        except Exception as e:
            await session.rollback()
            print(e)
            return {
                'message' : 'Something went wrong please try again'
            }