import redis.asyncio as redis
import time

#redis config
redis_client = redis.from_url("redis://localhost:6379" , encoding = "utf_8" , decode_responses = True)

async def rate_limited(key : str , limit : int , time_window : int) -> bool:
    current =  await redis_client.incr(key)

    if current==1:
        await redis_client.set(key , 1 , ex=time_window)
    
    if current <= limit:
        return True
    else:
        return False