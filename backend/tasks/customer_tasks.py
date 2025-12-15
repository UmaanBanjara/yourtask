from backend.utils.celery_app import celery_app
from backend.utils.smtp import send_mail
import asyncio
from backend.routes.customers import get_all_customers

@celery_app.task
#welcome message for customers
async def send_welcome_message(user_id : int , email : str):
    try:
        email = await(send_mail(
            subject="Welcome Message",
            body="This is a simple Welcome Message",
            to=[email]

        ))

        return{
            "message" : "Welcome Message Sent Successfully"
        }
    except Exception as e:
        return{
            "message" : "Something went wrong"
        }

@celery_app.task
#send customer details everyday
async def send_customer_details():
    customers = await get_all_customers(page=1 , limit=1000)
    if not customers:
        return {"message": "No Customers Yet"}

    body = "\n".join([f"{c['name']} - {c['phone']}" for c in customers])
    
    await send_mail(
        subject="Daily Customer Report",
        body=body,
        to=["umaanflutter@gmail.com"]
    )

    return {"message": "Customer details sent successfully"}
