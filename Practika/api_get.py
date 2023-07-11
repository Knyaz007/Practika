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


from fastapi import Path
 

# -------------------------------------------- Пользователи (Users) --------------------------------------------

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


@app.get("/users/{user_id}", tags=["Users"], response_model=User)
def get_user(user_id: int = Path(..., description="The ID of the user")) -> User:
    """
    Get tasks for a specific user by user_id.
 .
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
            return {"message": "User not found"}


@app.get("/users/{user_id}/tasks", tags=["Users"], response_model=List[Task])
def get_user_tasks(user_id: int = Path(..., description="The ID of the user")) -> List[Task]:
    with session_scope(Session) as session:
        db_tasks = session.query(DBTask).filter(DBTask.user_id == user_id).all()
        tasks_data: List[Task] = [
            Task(
                task_id=db_task.task_id,
                name=db_task.name,
                email=db_task.iv_priority                 
            )
            for db_task in db_tasks
        ]
        return tasks_data             



#@app.get("/users/{user_id}/group_tasks", tags=["Users"], response_model=List[Dict[str, Union[int, str, datetime]]])
#def get_user_group_tasks(user_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
#    with session_scope(Session) as session:
#        group_tasks = session.query(GroupTask).join(Task).filter(Task.user_id == user_id).all()
#        group_tasks_data = [
#            {"id": group_task.group_task_id, "title": group_task.name,
#             "created_at": group_task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            for group_task in group_tasks
#        ]
#        return group_tasks_data


#@app.get("/users/{user_id}/comments", tags=["Users"], response_model=List[Dict[str, Union[int, str, datetime]]])
#def get_user_comments(user_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
#    with session_scope(Session) as session:
#        comments = session.query(Comment).filter(Comment.user_id == user_id).all()
#        comments_data = [
#            {"id": comment.com_id, "text": comment.text, "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            for comment in comments
#        ]
#        return comments_data


#@app.get("/group_tasks", tags=["GroupTask"], response_model=List[Dict[str, Union[int, str, datetime]]])
#def get_group_tasks() -> List[Dict[str, Union[int, str, datetime]]]:
#    with session_scope(Session) as session:
#        group_tasks = session.query(GroupTask).all()
#        group_tasks_data = [
#            {"id": group_task.group_task_id, "description": group_task.description,
#             "created_at": group_task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            for group_task in group_tasks
#        ]
#        return group_tasks_data


#@app.get("/group_tasks/{group_task_id}", tags=["GroupTask"], response_model=Dict[str, Union[int, str, datetime]]])
#def get_group_task(group_task_id: int) -> Dict[str, Union[int, str, datetime]]:
#    with session_scope(Session) as session:
#        group_task = session.query(GroupTask).filter(GroupTask.group_task_id == group_task_id).first()
#        if group_task:
#            group_task_data = {"id": group_task.group_task_id, "name": group_task.name,
#                               "created_at": group_task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            return group_task_data
#        else:
#            return {"message": "Group task not found"}


#@app.get("/group_tasks/{group_task_id}/tasks", tags=["GroupTask"], response_model=List[Dict[str, Union[int, str, datetime]]])
#def get_group_tasks_tasks(group_task_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
#    with session_scope(Session) as session:
#        tasks = session.query(Task).filter(Task.group_task_id == group_task_id).all()
#        tasks_data = [
#            {"id": task.task_id, "name": task.name, "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            for task in tasks
#        ]
#        return tasks_data


#@app.get("/tasks", tags=["Task"], response_model=List[Dict[str, Union[int, str, datetime]]])
#def get_tasks() -> List[Dict[str, Union[int, str, datetime]]]:
#    with session_scope(Session) as session:
#        tasks = session.query(Task).all()
#        tasks_data = [
#            {"id": task.task_id, "name": task.name, "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            for task in tasks
#        ]
#        return tasks_data


#@app.get("/tasks/{task_id}", tags=["Task"], response_model=Dict[str, Union[int, str, datetime]]])
#def get_task(task_id: int) -> Dict[str, Union[int, str, datetime]]:
#    with session_scope(Session) as session:
#        task = session.query(Task).filter(Task.task_id == task_id).first()
#        if task:
#            task_data = {"id": task.task_id, "title": task.title,
#                         "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            return task_data
#        else:
#            return {"message": "Task not found"}


#@app.get("/tasks/{task_id}/user", tags=["Task"], response_model=List[Dict[str, Union[int, str, datetime]]])
#def get_task_users(task_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
#    with session_scope(Session) as session:
#        users = session.query(User).join(Task).filter(Task.task_id == task_id).all()
#        users_data = [
#            {"id": user.user_id, "name": user.name, "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            for user in users
#        ]
#        return users_data


#@app.get("/comments", tags=["Comments"], response_model=List[Dict[str, Union[int, str, datetime]]])
#def get_comments() -> List[Dict[str, Union[int, str, datetime]]]:
#    with session_scope(Session) as session:
#        comments = session.query(Comment).all()
#        comments_data = [
#            {"id": comment.com_id, "text": comment.text, "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            for comment in comments
#        ]
#        return comments_data


#@app.get("/comments/{comment_id}", tags=["Comments"], response_model=Dict[str, str]])
#def get_comment(comment_id: int) -> Dict[str, str]:
#    with session_scope(Session) as session:
#        comment = session.query(Comment).filter(Task.task_id == comment_id).first()
#        if comment:
#            comment_data = {"id": comment.com_id, "text": comment.text,
#                            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            return comment_data
#        else:
#            return {"message": "Comment not found"}


#@app.get("/group_tasks/tasks", tags=["GroupTask"], response_model=List[Dict[str, Union[int, str, datetime]]])
#def get_group_tasks_tasks() -> List[Dict[str, Union[int, str, datetime]]]:
#    with session_scope(Session) as session:
#        tasks = session.query(Task).all()
#        tasks_data = [
#            {"id": task.task_id, "name": task.name, "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            for task in tasks
#        ]
#        return tasks_data


#@app.get("/group_tasks/{group_task_id}/tasks/{task_id}", tags=["GroupTask"], response_model=Dict[str, Union[int, str, datetime]]])
#async def get_group_task_task(group_task_id: int, task_id: int) -> Dict[str, Union[int, str, datetime]]:
#    with session_scope(Session) as session:
#        task = session.query(Task).filter_by(group_task_id=group_task_id, task_id=task_id).first()
#        if task:
#            task_data = {"id": task.task_id, "name": task.name,
#                         "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            return task_data
#        else:
#            return {"message": "Task not found"}


#@app.get("/group_tasks/{group_task_id}/tasks/{task_id}/comments", tags=["GroupTask"], response_model=List[Dict[str, Union[int, str, datetime]]])
#async def get_group_task_task_comments(group_task_id: int, task_id: int) -> List[Dict[str, Union[int, str, datetime]]]:
#    with session_scope(Session) as session:
#        comments = session.query(Comment).filter(Comment.task_id == task_id).all()
#        comments_data = [
#            {"id": comment.com_id, "text": comment.text, "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")}
#            for comment in comments
#        ]
#        return comments_data
