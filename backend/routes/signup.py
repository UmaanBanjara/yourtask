from fastapi import APIRouter, HTTPException , Request
from pydantic import BaseModel, EmailStr, field_validator
import re
from backend.utils.rate_limiter import rate_limited
from backend.CRUD.signup import create_user

class Usercheck(BaseModel):
    username: str
    email: EmailStr
    password: str

    # Email validation should be inside the class
    @field_validator('email')
    def validate_email(cls, email):
        if not email.endswith('@gmail.com'):
            raise ValueError('Email must end with @gmail.com')
        return email

    # Password validation should also be inside the class
    @field_validator('password')
    def validate_password(cls, password):
        # Password must contain at least one digit
        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one number")
        
        # Password must contain at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one capital letter")
        
        # Password must contain at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character")
        
        # Password length should be at least 8 characters
        if len(password) < 8:
            raise ValueError("Password should be at least 8 characters long")
        
        return password


router = APIRouter()

@router.post('/signup')
async def signup(user: Usercheck , request : Request):
    #get client ip
    client_ip = request.client.host

    #apply rate limit
    allowed = await rate_limited(
        key=f"signup:{client_ip}", 
        limit=3, #3 request per hour
        time_window=60*60 #1 hour

    )

    if not allowed:
        raise HTTPException(status_code=401 , detail="Too many signup attempts. Try again later after sometime")
    try:
        # Assuming you have a function to create the user
        new_user = await create_user(
            user.username,
            user.email,
            user.password
        )
        
        if 'userId' not in new_user:
            return {
                'message': new_user['message']
            }
        return {
            'message': new_user['message'],
            'userId': new_user['userId'],
            'email': new_user['email']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
