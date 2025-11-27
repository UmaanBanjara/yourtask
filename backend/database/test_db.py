import os
from dotenv import load_dotenv
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy import text

load_dotenv() #load env

url = os.getenv('DATABASE_URL') #get env
print(url)
base = declarative_base()

engine = create_async_engine(url , echo=True) #engine creation

mysession = sessionmaker(
    engine , expire_on_commit=False , class_=AsyncSession
)

#test connection

async def test_connection():
    try:
        async with mysession() as session:
            result = await session.execute(text('SELECT 1'))
            print('Connection Successfull',result)
    except Exception as e:
        print('Something went wrong',e)

    
#test function

if __name__ == '__main__':
    asyncio.run(test_connection())
