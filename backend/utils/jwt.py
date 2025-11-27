import jwt
from jwt import ExpiredSignatureError , PyJWTError
import os
import datetime
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#creating access token
def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        'exp' : expire
    })
    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)
    return encoded_jwt

#verifying access token
def verify_access_token(token : str):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        id : int = payload.get("id")
        if id is None:
            return {
                'message' : 'Invalid Token'
            }
        
        return id
    except ExpiredSignatureError:
        return {
            'message' : 'Token Expired'
        }
    except PyJWTError:
        return {
            'message' : 'Invalid Token'
        }