from fastapi import APIRouter , HTTPException
from backend.tasks.test_tasks import test_task


router =  APIRouter()

@router.get('/test-celery')
async def test_test():
    task = test_task.delay()
    return{
        "message" : "Task sent to celery",
        "id" : task.id
    }