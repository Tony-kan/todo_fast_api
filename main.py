from fastapi import FastAPI, APIRouter, HTTPException
from config import collection
from database.schemas import all_tasks, individual_task
from database.models import Todo
from bson.objectid import ObjectId
from datetime import datetime

app = FastAPI()
todo_router = APIRouter()

# api request to get all the todos from the db


@todo_router.get("")
async def get_all_todos():
    todos = collection.find({"is_deleted": False})
    return all_tasks(todos)

# api request to create a new todo into the db


@todo_router.post("/")
async def create_task(new_task: Todo):
    try:
        res = collection.insert_one(dict(new_task))
        return {"status_code": 200, "id": str(res.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error : {e}")


# api request to update the todo task
@todo_router.put("/{task_id}")
async def update_task(task_id: str, updated_task: Todo):
    try:
        id = ObjectId(task_id)
        existing_task = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_task:
            return HTTPException(status_code=404, detail=f"Task does not exist")
        updated_task.updated_at = datetime.timestamp(datetime.now())
        res = collection.update_one({"_id": id}, {"$set": dict(updated_task)})
        return {"status_code": 200, "message": "Task updated successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error : {e}")


# api request to delete a task from db
@todo_router.delete("/{task_id}")
async def delete_task(task_id: str):
    try:
        id = ObjectId(task_id)
        existing_task = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_task:
            return HTTPException(status_code=404, detail=f"Task does not exist")

        # soft delete,for hard delete(permanent)=use delete_one
        updated_task.updated_at = datetime.timestamp(datetime.now())
        res = collection.update_one(
            {"_id": id}, {"$set": {"is_deleted": True}})
        return {"status_code": 200, "message": "Task Deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error : {e}")


app.include_router(todo_router, prefix="/api/v1/todos")
