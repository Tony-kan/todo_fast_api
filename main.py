from fastapi import FastAPI, APIRouter
from config import collection
from database.schemas import all_tasks, individual_task
from database.models import Todo

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


app.include_router(todo_router, prefix="/api/v1/todos")
