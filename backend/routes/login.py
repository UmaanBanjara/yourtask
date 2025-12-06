from fastapi import APIRouter , HTTPException , Request
from backend.CRUD.login import verify_user
from pydantic import BaseModel , EmailStr
from backend.utils.rate_limiter import rate_limited

class Usercheck(BaseModel):
    email : EmailStr
    password : str

router = APIRouter()

@router.post('/login')
async def login(user : Usercheck , request : Request):
        user_ip = request.client.host
        allowed = await rate_limited(
             key=f"login:{user_ip}",
             limit=3,
             time_window=60*60
        )
        if not allowed:
             raise HTTPException(status_code=401 , detail="Too many login attemps. Please try again later sometime")
        verify = await verify_user(email=user.email , password=user.password)
        if 'access_token' not in verify:
            raise HTTPException(status_code=400 , detail=verify['message'])
        return verify
        