# -*- coding: windows-1251 -*-
from fastapi import FastAPI


from fastapi.openapi.utils import get_openapi
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker  
from migration import db
import schemas
import models

from typing import List, Dict, Union
from datetime import datetime

DBUser = models.User
DBGroupTask = models.GroupTask
DBComment = models.Comment
DBTask = models.Task

User = schemas.User
GroupTask = schemas.GroupTask
Comment = schemas.Comment
Task = schemas.Task


# Создаем соединение с базой данных
engine = create_engine(db.original_location)
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

from contextlib import contextmanager
@contextmanager
def session_scope(Session):
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()



# Определите свои пути и операции здесь

# Функция для получения Swagger-схемы
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API description",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Маршрут для получения Swagger-схемы
@app.get("/openapi.json")
async def get_openapi_endpoint():
    return custom_openapi()


from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": "Validation Error"}
    )


# -------------------------------------------- Пользователи (Users) --------------------------------------------
from fastapi import Path

# Определяем маршрут для получения пользователей
# Определяем маршрут для получения пользователей
@app.get("/users", tags=["Users"], response_model=List[User])
def get_users() -> List[User]:
    with session_scope(Session) as session:
        db_users = session.query(DBUser).all()
        users_data: List[User] = [
            User(
                user_id=db_user.user_id,
                name=db_user.name,
                email=db_user.email,
                password=db_user.password,
                created_at=db_user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                update_at=db_user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            )
            for db_user in db_users
        ]
        return users_data

@app.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: int = Path(..., description="The ID of the user")) -> User:
    """
    Get a specific user by user_id.
    """
    with session_scope(Session) as session:
       db_user = session.query(DBUser).filter(DBUser.user_id == user_id).first()
       if db_user:
           user_data = User(
                user_id=db_user.user_id,
                name=db_user.name,
                email=db_user.email,
                password=db_user.password,
                created_at=db_user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                update_at=db_user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            )
           return user_data
       else:
           raise HTTPException(status_code=404, detail="User not found")


@app.post("/users", tags=["Users"])
async def create_user() -> Dict[str, str]:
    """
    Create a new user.
    """
    return {"message": "Create a new user"}


@app.put("/users/{user_id}", tags=["Users"])
async def update_user(user_id: int) -> Dict[str, str]:
    """
    Update a user by user_id.

    Parameters:
    - user_id (int): The ID of the user.
    """
    return {"message": f"Update user {user_id}"}


@app.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int) -> Dict[str, str]:
    """
    Delete a user by user_id.

    Parameters:
    - user_id (int): The ID of the user.
    """
    return {"message": f"Delete user {user_id}"}


@app.get("/users/{user_id}/tasks", tags=["Users"])
def get_user_tasks(user_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get tasks for a specific user by user_id.

    Parameters:
    - user_id (int): The ID of the user.
    """
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    tasks_data = [{"id": task.task_id, "title": task.name, "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
                  for task in tasks]
    return tasks_data


@app.get("/users/{user_id}/group_tasks", tags=["Users"])
def get_user_group_tasks(user_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get group tasks for a specific user by user_id.

    Parameters:
    - user_id (int): The ID of the user.
    """
    group_tasks = session.query(GroupTask).join(Task).filter(Task.user_id == user_id).all()
    group_tasks_data = [{"id": group_task.group_task_id, "title": group_task.name,
                         "created_at": group_task.created_at.strftime("%Y-%m-%d %H:%M:%S")} for group_task in
                        group_tasks]
    return group_tasks_data


@app.get("/users/{user_id}/comments", tags=["Users"])
def get_user_comments(user_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get comments for a specific user by user_id.

    Parameters:
    - user_id (int): The ID of the user.
    """
    comments = session.query(Comment).filter(Comment.user_id == user_id).all()
    comments_data = [
        {"id": comment.com_id, "text": comment.text, "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")} for
        comment in comments]
    return comments_data


# ------------------------------------  Группы задач (GroupTask) ---------------------------------------
@app.get("/group_tasks", tags=["GroupTask"])
def get_group_tasks() -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get all group tasks.
    """
    group_tasks = session.query(GroupTask).all()
    group_tasks_data = [{"id": group_task.group_task_id, "description": group_task.description,
                         "created_at": group_task.created_at.strftime("%Y-%m-%d %H:%M:%S")} for group_task in
                        group_tasks]
    return group_tasks_data


@app.get("/group_tasks/{group_task_id}/", tags=["GroupTask"])
def get_group_task(group_task_id: int) -> Dict[str, Union[int, str, datetime]]:
    """
    Get a specific group task by group_task_id.

    Parameters:
    - group_task_id (int): The ID of the group task.
    """
    group_task = session.query(GroupTask).filter(GroupTask.group_task_id == group_task_id).first()
    if group_task:
        group_task_data = {"id": group_task.group_task_id, "name": group_task.name,
                           "created_at": group_task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
        return group_task_data
    else:
        return {"message": "Group task not found"}


@app.post("/group_tasks", tags=["GroupTask"])
async def create_group_task() -> Dict[str, str]:
    """
    Create a new group task.
    """
    return {"message": "Create a new group task"}


@app.put("/group_tasks/{group_task_id}", tags=["GroupTask"])
async def update_group_task(group_task_id: int) -> Dict[str, str]:
    """
    Update a group task by group_task_id.

    Parameters:
    - group_task_id (int): The ID of the group task.
    """
    return {"message": f"Update group task {group_task_id}"}


@app.delete("/group_tasks/{group_task_id}", tags=["GroupTask"])
async def delete_group_task(group_task_id: int) -> Dict[str, str]:
    """
    Delete a group task by group_task_id.

    Parameters:
    - group_task_id (int): The ID of the group task.
    """
    return {"message": f"Delete group task {group_task_id}"}


@app.get("/group_tasks/{group_task_id}/tasks", tags=["GroupTask"])
def get_group_tasks_tasks(group_task_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get tasks for a specific group task by group_task_id.

    Parameters:
    - group_task_id (int): The ID of the group task.
    """
    tasks = session.query(Task).filter(Task.group_task_id == group_task_id).all()
    tasks_data = [{"id": task.task_id, "name": task.name, "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
                  for task in tasks]
    return tasks_data


# Задачи (Task)
@app.get("/tasks", tags=["Task"])
def get_tasks() -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get all tasks.
    """
    tasks = session.query(Task).all()
    tasks_data = [{"id": task.task_id, "name": task.name, "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
                  for task in tasks]
    return tasks_data


@app.get("/tasks/{task_id}", tags=["Task"])
def get_task(task_id: int) -> Dict[str, Union[int, str, datetime]]:
    """
    Get a specific task by task_id.

    Parameters:
    - task_id (int): The ID of the task.
    """
    task = session.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task_data = {"id": task.task_id, "title": task.title,
                     "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
        return task_data
    else:
        return {"message": "Task not found"}


@app.post("/tasks", tags=["Task"])
async def create_task() -> Dict[str, str]:
    """
    Create a new task.
    """
    return {"message": "Create a new task"}


@app.put("/tasks/{task_id}", tags=["Task"])
async def update_task(task_id: int) -> Dict[str, str]:
    """
    Update a task by task_id.

    Parameters:
    - task_id (int): The ID of the task.
    """
    return {"message": f"Update task {task_id}"}


@app.delete("/tasks/{task_id}", tags=["Task"])
async def delete_task(task_id: int) -> Dict[str, str]:
    """
    Delete a task by task_id.

    Parameters:
    - task_id (int): The ID of the task.
    """
    return {"message": f"Delete task {task_id}"}


@app.get("/tasks/{task_id}/user", tags=["Task"])
def get_task_users(task_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get user for a specific task by task_id.

    Parameters:
    - task_id (int): The ID of the task.
    """
    users = session.query(User).join(Task).filter(Task.task_id == task_id).all()
    users_data = [{"id": user.user_id, "name": user.name, "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")}
                  for user in users]
    return users_data


# --------------------------------------------- Комментарии (Comments) --------------------------------------------

@app.get("/comments", tags=["Comments"])
def get_comments() -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get all comments.
    """
    comments = session.query(Comment).all()
    comments_data = [
        {"id": comment.com_id, "text": comment.text, "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")} for
        comment in comments]
    return comments_data


@app.get("/comments/{comment_id}", tags=["Comments"])
def get_comment(comment_id: int) -> Dict[str, str]:
    """
    Get a specific comment by comment_id.

    Parameters:
    - comment_id (int): The ID of the comment.
    """
    comments = session.query(Comment).filter(Task.task_id == comment_id).first()
    if comments:
        task_data = {"id": comments.com_id, "text": comments.text,
                     "created_at": comments.created_at.strftime("%Y-%m-%d %H:%M:%S")}
        return task_data
    else:
        return {"message": "Task not found"}


@app.post("/comments", tags=["Comments"])
async def create_comment() -> Dict[str, str]:
    """
    Create a new comment.
    """
    return {"message": "Create a new comment"}


@app.delete("/comments/{comment_id}", tags=["Comments"])
async def delete_comment(comment_id: int) -> Dict[str, str]:
    """
    Delete a comment by comment_id.

    Parameters:
    - comment_id (int): The ID of the comment.
    """
    return {"message": f"Delete comment {comment_id}"}


# ------------------------  Группы задач и их связи с задачами и комментариями  -------------------------------------

@app.get("/group_tasks/tasks", tags=["GroupTask"])
def get_group_tasks_tasks() -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get all tasks from all group tasks.
    """
    tasks = session.query(Task).all()
    tasks_data = [{"id": task.task_id, "name": task.name, "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
                  for task in tasks]
    return tasks_data


@app.get("/group_tasks/{group_task_id}/tasks/{task_id}", tags=["GroupTask"])
async def get_group_task_task(group_task_id: int, task_id: int) -> Dict[str, Union[int, str, datetime]]:
    """
    Get a specific task from a specific group task.

    Parameters:
    - group_task_id (int): The ID of the group task.
    - task_id (int): The ID of the task.
    """

    task = session.query(Task).filter_by(group_task_id=group_task_id, task_id=task_id).first()
    if task:
        task = {"id": task.task_id, "name": task.name,
                "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
        return task
    else:
        return {"message": "Task not found"}


@app.get("/group_tasks/{group_task_id}/tasks/{task_id}/comments", tags=["GroupTask"])
async def get_group_task_task_comments(group_task_id: int, task_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
    """
    Get comments for a specific task in a specific group task.

    Parameters:
    - group_task_id (int): The ID of the group task.
    - task_id (int): The ID of the task.
    """
    comments = session.query(Comment).filter(Comment.task_id == task_id).all()
    comments_data = [
        {"id": comment.com_id, "text": comment.text, "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")} for
        comment in comments]
    return comments_data
