import redis.asyncio as redis
import json

#redis config
redis_cache_client = redis.from_url("redis://localhost:6379" , encoding = "utf-8" , decode_responses = True)

async def set_cache(key : str , value : dict , time_window : int = 60):
    #store value in redis with time to live
    await redis_cache_client.set(key , value=json.dumps(value) , ex = time_window)

async def get_cache(key : str) -> dict | None :
    #get value from redis
    data = await redis_cache_client.get(key)
    if data:
        return json.loads(data)
    return None

async def delete_cache(key : str):
    #delete the key
    await redis_cache_client.delete(key)