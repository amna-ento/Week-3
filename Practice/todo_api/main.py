from fastapi import FastAPI, HTTPException, APIRouter, Depends, status
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


# -----------------------------
# Pydantic Request/Response Models
# -----------------------------

class Todo(BaseModel):
    task: str = Field(
        min_length=3,
        max_length=100,
        description="Enter the task you want to complete."
    )
    completed: Optional[bool] = False


class TodoResponse(BaseModel):
    id: int
    task: str
    completed: bool


# -----------------------------
# Fake Database
# -----------------------------

todos = [
    {
        "id": 1,
        "task": "Learn FastAPI",
        "completed": False
    },
    {
        "id": 2,
        "task": "Learn CRUD",
        "completed": False
    }
]


# -----------------------------
# Dependency Injection
# -----------------------------

def verify_request():
    return "Request Verified"


# -----------------------------
# APIRouter
# -----------------------------

router = APIRouter(prefix="/todos", tags=["Todos"])


# -----------------------------
# GET
# Query Parameters
# Dependency Injection
# Response Model
# -----------------------------

@router.get("/", response_model=list[TodoResponse])
def get_todos(
    completed: Optional[bool] = None,
    message: str = Depends(verify_request)
):
    if completed is None:
        return todos

    return [todo for todo in todos if todo["completed"] == completed]


# -----------------------------
# GET
# Path Parameters
# -----------------------------

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):

    for todo in todos:
        if todo["id"] == todo_id:
            return todo

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )


# -----------------------------
# POST
# Request Body
# Advanced Status Code
# -----------------------------

@router.post(
    "/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo(todo: Todo):

    new_todo = {
        "id": len(todos) + 1,
        "task": todo.task,
        "completed": todo.completed
    }

    todos.append(new_todo)

    return new_todo


# -----------------------------
# PUT
# -----------------------------

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updated_todo: Todo):

    for todo in todos:

        if todo["id"] == todo_id:
            todo["task"] = updated_todo.task
            todo["completed"] = updated_todo.completed
            return todo

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )


# -----------------------------
# DELETE
# -----------------------------

@router.delete("/{todo_id}")
def delete_todo(todo_id: int):

    for todo in todos:

        if todo["id"] == todo_id:
            todos.remove(todo)
            return {
                "message": "Todo deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found"
    )


# -----------------------------
# Custom Exception
# -----------------------------

class InvalidTodoException(Exception):
    pass


@app.exception_handler(InvalidTodoException)
async def invalid_todo_handler(request, exc):
    return {
        "message": "Custom Exception Triggered"
    }


@router.get("/error/test")
def trigger_error():
    raise InvalidTodoException()


# Register Router
app.include_router(router)