from fastapi import APIRouter , Request , HTTPException , Depends
from backend.schemas.customers import CustomerCheck
from backend.schemas.updatecustomers import UpdateCustomerCheck
from backend.CRUD.customers import create_new_customer , get_customer_by_id , delete_customer_by_id , update_customer_by_id, get_all_customers
from backend.utils.rate_limiter import rate_limited
from backend.utils.verify_token import get_current_user
from backend.utils.redis_caching import get_cache , set_cache , delete_cache

router = APIRouter()

async def invalidate_customer_cache():
    for page in range(1,11):
        for limit in [10 , 20 , 30]:
            cache_key = f"customers:page{page}:limit{limit}"
            await delete_cache(cache_key)

@router.post('/create/customer')
async def create_customer(customer : CustomerCheck , request : Request , user_id : int = Depends(get_current_user)):
    client_ip = request.client.host

    allowed = await rate_limited(
        key=f"createcustomer:{client_ip}",
        limit=3,
        time_window=60*60
    )
    if not allowed:
        raise HTTPException(status_code=401 , detail="Too many attempts. please try again later sometime")
    result = await create_new_customer(customer=customer)
    await invalidate_customer_cache()
    return result


@router.get('/get/customer/{Customerid}')
async def get_customer(Customerid : int , request : Request , user_id : int = Depends(get_current_user)):
    client_ip = request.client.host

    allowed = await rate_limited(
        key=f"getcustomerid:{client_ip}",
        limit=3,
        time_window=60*60
    )
    if not allowed:
        raise HTTPException(status_code=401 , detail='Too many attempts. Please try again later sometime')
    result = await get_customer_by_id(Customerid)
    return result

@router.delete('/delete/customer/{customerid}')
async def deletecustomer(customerid : int , request : Request , user_id : int = Depends(get_current_user)):
    client_ip = request.client.host

    allowed = await rate_limited(
        key = f"deletecustomer:{client_ip}",
        limit=3,
        time_window=60*60
    )
    if not allowed:
        raise HTTPException(status_code=401 , detail='Too many attempts. please try again later sometime')
    
    result = await delete_customer_by_id(customerid)
    await invalidate_customer_cache()
    return result

@router.patch('/update/customer/{customerid}')
async def updatecustomer(customerid : int , request : Request , data : UpdateCustomerCheck , user_id : int = Depends(get_current_user)):
    client_ip = request.client.host

    allowed = await rate_limited(
        key=f"updatecustomer:{client_ip}",
        limit=3,
        time_window=60*60
    )
    if not allowed:
        raise HTTPException(status_code=401 , detail='Too many attemps. please try again later sometime')
    result = await update_customer_by_id(customerid , data)
    await invalidate_customer_cache()
    return result

@router.get('/customers')
async def get_customers(request : Request ,page : int = 1 , limit : int = 20 , user_id : int = Depends(get_current_user)):
    client_ip = request.client.host
    allowed = await rate_limited(
        key=f"getcustomer:{client_ip}",\
        limit=3,
        time_window=60*60
    )
    if not allowed:
        raise HTTPException(status_code=401 , detail='Too many attempts. Please try again later sometime')
    #max limit
    Max_Limit = 50
    limit = min(limit , Max_Limit)

    #cache key
    cache_key = f"customers:page{page}:limit{limit}"
    #check if cache exits or not
    cached = await get_cache(cache_key)
    if cached:
        return{
            "source" : "cache",
            "data" : cached
        }
    
    #cache miss , fetch from db
    data = await get_all_customers(page=page , limit=limit)

    #save to cache(ttl - time to live necessary)
    await set_cache(cache_key , value=data , time_window=60) #60 seconds

    return{
        "source" : "db",
        "data" : data
    }

