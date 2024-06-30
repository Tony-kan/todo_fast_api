from fastapi import FastAPI, APIRouter
from config import collection
from database.schemas import all_tasks, individual_task
from database.models import Todo
from bson.objectid import ObjectId
from datetime import datetime

app = FastAPI()
todo_router = APIRouter()


@todo_router.get("")
async def get_all_todos():
    todos = collection.find()
    return all_tasks(todos)


@todo_router.post("/")
async def create_task(new_task: Todo):
    try:
        res = collection.insert_one(dict(new_task))
        return {"status_code": 200, "id": str(res.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error : {e}")


@todo_router.put("/{task_id}")
async def update_task(task_id: str, updated_task: Todo):
    try:
        id = ObjectId(task_id)
        existing_task = collection.find_one({"id": id, "is_deleted": False})
        if not existing_task:
            return HTTPException(status_code=404, detail=f"Task does not exist")
        updated_task.updated_at = datetime.timestamp(datetime.now())
        res = collection.update_one({"id": id}, {"$set": dict(updated_task)})
        return {"status_code": 200, "message": "Task updated successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error : {e}")


app.include_router(todo_router, prefix="/api/v1/todos")
