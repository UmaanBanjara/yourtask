from fastapi import APIRouter , HTTPException, Request
from backend.CRUD.resendotp import resend_otp
from pydantic import BaseModel , EmailStr
from backend.utils.rate_limiter import rate_limited


class Usercheck(BaseModel):
    email : EmailStr
    userId : int

router = APIRouter()

@router.post('/resend/otp')
async def otp_resend(otp : Usercheck , request : Request):
    user_ip = request.client.host
    allowed = await rate_limited(
        key = f"resentotp:{user_ip}",
        limit=2,
        time_window=60*60
    )
    if not allowed:
        raise HTTPException(status_code=401 , detail="Too many attemps. Please try again later sometime")
    otpresend = await resend_otp(
        email=otp.email,
        userId=otp.userId
    )
    if otpresend['message'] != 'OTP resend successfully':
         raise HTTPException(status_code=400, detail=otpresend['message'])
    return{
        'message' : otpresend['message']
    }