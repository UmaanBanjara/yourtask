from fastapi import APIRouter , HTTPException
from backend.CRUD.verifyotp import verify_otp
from pydantic import BaseModel


class UserCheck(BaseModel):
    userId : int
    code : str

router  = APIRouter()

@router.post('/otp/verify')

async def otpverify(otpcheck : UserCheck):
    otp_verify = await verify_otp(
        otpcheck.code,
        otpcheck.userId
    )

    if otp_verify['message'] != 'OTP verified successfully':
        return {
            'message' : otp_verify['message']
        }
    return {
        'message' : otp_verify['message']
    }