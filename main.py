from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.signup import router as signup_router
from backend.routes.login import router as login_router
from backend.routes.verifyotp import router as verifyotp_router
from backend.routes.resendotp import router as resendotp_router
from backend.routes.customers import router as customer_router
from backend.routes.test_celery import router as test_celery_router


app = FastAPI(title='YourTask')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(signup_router , prefix='/auth' , tags = ['Authorization'])
app.include_router(login_router , prefix='/auth' , tags = ['Authorization'])
app.include_router(verifyotp_router , prefix = '/auth' , tags = ['Authorization'])
app.include_router(resendotp_router , prefix = '/auth' , tags = ['Authorization'])
app.include_router(customer_router, prefix='/customers' , tags=['Customers'])
app.include_router(test_celery_router , prefix='/celery' , tags=['Celery'])

#root endpoint
@app.get('/')
async def root():
    return {
        'message' : 'Welcome to YourTask'
    }