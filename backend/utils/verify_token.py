from fastapi import HTTPException, Request
from backend.utils.jwt import verify_access_token


#function to get current user
async def get_current_user(request : Request):
    token = request.headers.get('Authorization')

    if not token:
        raise HTTPException(status_code=401 , detail='Token Not Found')
    
    try:
        token = token.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401 , detail='Invalid token format')
    
    user_id_or_error = verify_access_token(token)

    if isinstance(user_id_or_error , dict):
        raise HTTPException(status_code=401 , detail=user_id_or_error['message'])
    return user_id_or_error