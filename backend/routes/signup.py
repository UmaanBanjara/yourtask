from fastapi import APIRouter , HTTPException
from pydantic import BaseModel , EmailStr
from backend.CRUD.signup import create_user

class Usercheck(BaseModel):
    username : str
    email : EmailStr
    password : str

router = APIRouter()

@router.post('/signup')

async def signup(user : Usercheck):
    try:
        new_user = await create_user(
            user.username,
            user.email,
            user.password
        )
        
        if 'userId' not in new_user:
            return {
                'message' : new_user['message']
            }
        return {
            'message' : new_user['message'],
            'userId' : new_user['userId'],
            'email' : new_user['email']
        }
    except Exception as e:
        raise HTTPException(status_code=400 , detail=str(e))