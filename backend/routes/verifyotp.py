from fastapi import APIRouter , HTTPException, Request
from backend.CRUD.verifyotp import verify_otp
from pydantic import BaseModel
from backend.utils.rate_limiter import rate_limited


class UserCheck(BaseModel):
    userId : int
    code : str

router  = APIRouter()

@router.post('/otp/verify')

async def otpverify(otpcheck : UserCheck , request : Request):
    user_ip = request.client.host
    allowed = await rate_limited(
        key=f"verifyotp:{user_ip}",
        limit=2,
        time_window=60*60
    )
    if not allowed:
        raise HTTPException(status_code=401 , detail="Too many attemps. Please try again later sometime")
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