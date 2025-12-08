from backend.models.customers import Customer
from sqlalchemy.future import select
from backend.database.test_db import mysession
from backend.schemas.customers import CustomerCheck
from backend.schemas.updatecustomers import UpdateCustomerCheck

#function to create new customer
async def create_new_customer(customer : CustomerCheck):
    async with mysession() as session:
        try:
            new_customer = Customer(
                first_name = customer.first_name,
                last_name = customer.last_name,
                email = customer.email,
                address = customer.address,
                phone_number = customer.phone_number,
                city = customer.city
            )

            session.add(new_customer)
            await session.commit()
            await session.refresh(new_customer)

            return {
                'message' : 'Customer create successfully',
                'customerId' : new_customer.customer_id,
                'customerEmail' : new_customer.email
            }
        except Exception as e:
            await session.rollback()
            return {
                'message' : 'Something went wrong'
            }

#get customer by id
async def get_customer_by_id(Customerid : int):
    async with mysession() as session:
        try:
            result = await session.execute(select(Customer).where(Customer.customer_id == Customerid))
            customer = result.scalar_one_or_none()

            if customer is None:
                return{
                    'message' : 'Customer Not Found'
                }
            return {
                "customer_id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "phone_number": customer.phone_number,
                "address": customer.address,
                "city": customer.city,
                "created_at": customer.created_at
            }
        except Exception as e:
            return {
                'message' : 'Something went wrong'
            }

#delete customer by id
async def delete_customer_by_id(customerId : int):
    async with mysession() as session:
        try:
            result = await session.execute(select(Customer).where(Customer.customer_id == customerId))
            customer = result.scalar_one_or_none()

            if customer is None:
                return{
                    'message' : 'Customer Not Found'
                }
            await session.delete(customer)
            await session.commit()

            return{'message' : 'Customer Deleted Successfully'}
        
        except Exception as e:
            await session.rollback()
            return {
                'message' : 'Something went wrong'
            }
            
#update customer
async def update_customer_by_id(customerId : int , data : UpdateCustomerCheck):
    async with mysession() as session:
        try:
            result = await session.execute(select(Customer).where(Customer.customer_id == customerId))
            customer = result.scalar_one_or_none()

            if not customer:
                return{
                    'message' : 'Customer Not Found'
                }
            #convert pydantic model into sqlalchemy object
            update_data = data.dict(exclude_unset=True)

            for field, value in update_data.items():
                setattr(customer , field , value)
            
            await session.commit()
            await session.refresh(customer)

            return{
                "message": "Customer Updated Successfully",
                "customer": {
                    "id": customer.customer_id,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "email": customer.email,
                    "phone_number": customer.phone_number,
                    "address": customer.address,
                    "city": customer.city
                }}
        except Exception as e:
            return{
                'message' : 'Something went wrong'
            }