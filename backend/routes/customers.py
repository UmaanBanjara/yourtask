from fastapi import APIRouter , Request , HTTPException
from backend.schemas.customers import CustomerCheck
from backend.schemas.updatecustomers import UpdateCustomerCheck
from backend.CRUD.customers import create_new_customer , get_customer_by_id , delete_customer_by_id , update_customer_by_id
from backend.utils.rate_limiter import rate_limited

router = APIRouter()

@router.post('/create/customer')
async def create_customer(customer : CustomerCheck , request : Request):
    client_ip = request.client.host

    allowed = await rate_limited(
        key=f"createcustomer:{client_ip}",
        limit=3,
        time_window=60*60
    )
    if not allowed:
        raise HTTPException(status_code=401 , detail="Too many attempts. please try again later sometime")
    return await create_new_customer(customer=customer)


@router.get('/get/customer/{Customerid}')
async def get_customer(Customerid : int , request : Request):
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
async def deletecustomer(customerid : int , request : Request):
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
async def updatecustomer(customerid : int , request : Request , data : UpdateCustomerCheck):
    client_ip = request.client.host

    allowed = await rate_limited(
        key=f"updatecustomer:{client_ip}",
        limit=3,
        time_window=60*60
    )
    if not allowed:
        raise HTTPException(status_code=401 , detail='Too many attemps. please try again later sometime')
    return await update_customer_by_id(customerid , data)