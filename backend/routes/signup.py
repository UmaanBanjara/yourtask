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
        #if email already exits
        if 'user' not in new_user:
            raise HTTPException(status_code=400 , detail=new_user['message'])
        
        return {
            'message' : new_user['message'],
            'id' : new_user['user']['id'],
            'username' : new_user['user']['username']
        }
    except Exception as e:
        raise HTTPException(status_code=400 , detail=str(e))