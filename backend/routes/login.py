from fastapi import APIRouter , HTTPException
from backend.CRUD.login import verify_user
from pydantic import BaseModel , EmailStr

class Usercheck(BaseModel):
    email : EmailStr
    password : str

router = APIRouter()

@router.post('/login')
async def login(user : Usercheck):
        verify = await verify_user(email=user.email , password=user.password)
        if 'access_token' not in verify:
            raise HTTPException(status_code=400 , detail=verify['message'])
        return verify
        