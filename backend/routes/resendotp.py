from fastapi import APIRouter , HTTPException
from backend.CRUD.resendotp import resend_otp
from pydantic import BaseModel , EmailStr


class Usercheck(BaseModel):
    email : EmailStr
    userId : int

router = APIRouter()

@router.post('/resend/otp')
async def otp_resend(otp : Usercheck):
    otpresend = await resend_otp(
        email=otp.email,
        userId=otp.userId
    )
    if otpresend['message'] != 'OTP resend successfully':
         raise HTTPException(status_code=400, detail=otpresend['message'])
    return{
        'message' : otpresend['message']
    }