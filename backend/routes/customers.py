from fastapi import APIRouter , Request , HTTPException , Depends
from backend.schemas.customers import CustomerCheck
from backend.schemas.updatecustomers import UpdateCustomerCheck
from backend.CRUD.customers import create_new_customer , get_customer_by_id , delete_customer_by_id , update_customer_by_id, get_all_customers
from backend.utils.rate_limiter import rate_limited
from backend.utils.verify_token import get_current_user

router = APIRouter()

@router.post('/create/customer')
async def create_customer(customer : CustomerCheck , request : Request , user_id : int = Depends(get_current_user)):
    client_ip = request.client.host

    # allowed = await rate_limited(
    #     key=f"createcustomer:{client_ip}",
    #     limit=3,
    #     time_window=60*60
    # )
    # if not allowed:
    #     raise HTTPException(status_code=401 , detail="Too many attempts. please try again later sometime")
    return await create_new_customer(customer=customer)


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
    return await get_customer_by_id(Customerid)

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
    return await delete_customer_by_id(customerid)

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
    return await update_customer_by_id(customerid , data)

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
    return await get_all_customers(page=page , limit=limit)