import redis.asyncio as redis
import time

#redis config
redis_client = redis.from_url("redis://localhost:6379" , encoding = "utf_8" , decode_responses = True)

async def rate_limited(key : str , limit : int , time_window : int) -> bool:
    current =  await redis_client.incr(key)

    if current==1:
        await redis_client.expire(key , time_window)
        print(f"Key is : {key} created with expiration  : {time_window}")
    
    ttl = await redis_client.ttl(key)
    print(f"Time left for the key is {ttl}")
    
    if current <= limit:
        return True
    else:
        return False