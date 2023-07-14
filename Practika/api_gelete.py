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
        if db_users:
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
        else:
            return {"message": "Users not found"}


@app.get("/users/{user_id}", tags=["Users"], response_model=User)
def get_user(user_id: int = Path(..., description="The ID of the user")) -> User:
    """
    Get tasks for a specific user by user_id.
     
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
    """
    Get tasks for a specific user by user_id.
 .
    """
    with session_scope(Session) as session:
        db_tasks = session.query(DBTask).filter(DBTask.user_id == user_id).all()
        if db_tasks:
            tasks_data: List[Task] = [
            Task(           
                task_id=db_task.task_id,
                name=db_task.name,
                iv_priority=db_task.iv_priority,
                period_ofexecution=db_task.period_ofexecution,
                group_task_id=db_task.group_task_id,
                user_id=db_task.user_id,
                created_at=db_task.created_at,
                updated_at=db_task.updated_at,
                completed=db_task.completed                
            )
            for db_task in db_tasks
        ]
            return tasks_data  
        else:
            return {"message": "Task not found"}



@app.get("/users/{user_id}/group_tasks", tags=["Users"], response_model=List[GroupTask])
def get_user_group_tasks(user_id: int = Path(..., description="The ID of the user")) -> List[GroupTask]:
    """
    Get group tasks for a specific user by user_id.

    """
    with session_scope(Session) as session:
        group_tasks = session.query(DBGroupTask).filter(DBGroupTask.user_id == user_id).all()
        if group_tasks:
            group_tasks_data : List[GroupTask] = [
            GroupTask(
            group_task_id=group_task.task_id,
            name=group_task.task_id,
            description=group_task.task_id,
            user_id=group_task.task_id,
            created_at=group_task.task_id,
            updated_at=group_task.task_id,           
            )
            for group_task in group_tasks
        ]
            return group_tasks_data
        else:
            return {"message": "Group task not found"}


@app.get("/users/{user_id}/comments", tags=["Users"], response_model=List[Comment])
def get_user_comments(user_id: int = Path(..., description="The ID of the user")) -> List[Comment]:
    """
    Get comments for a specific user by user_id.

    """
    with session_scope(Session) as session:
        comments = session.query(DBComment).filter(DBComment.user_id == user_id).all()
        if comments:
            comments_data = List[Comment] = [
            Comment(
            com_id=comment.com_id,
            text=comment.text,
            task_id=comment.task_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            user_id=comment.user_id,
            )        
            for comment in comments
        ]
            return comments_data
        else:
            return {"message": "Comments not found"}

# ------------------------------------  Группы задач (GroupTask) ---------------------------------------

@app.get("/group_tasks", tags=["GroupTask"], response_model=List[GroupTask])
def get_group_tasks() -> List[GroupTask]:
    """
    Get all group tasks.
    """
    with session_scope(Session) as session:
        group_tasks = session.query(DBGroupTask).all()
        if group_tasks:
            group_tasks_data : List[GroupTask] = [
            GroupTask(
            group_task_id=group_task.task_id,
            name=group_task.task_id,
            description=group_task.task_id,
            user_id=group_task.task_id,
            created_at=group_task.task_id,
            updated_at=group_task.task_id,           
            )
            for group_task in group_tasks
        ]
            return group_tasks_data
        else:
            return {"message": "Group task not found"}


@app.get("/group_tasks/{group_task_id}", tags=["GroupTask"], response_model=List[GroupTask])
def get_group_task(group_task_id: int = Path(..., description="The ID of the Group tasks")) ->  List[GroupTask]:
    """
    Get a specific group task by group_task_id.

    """
    with session_scope(Session) as session:
        group_tasks = session.query(DBGroupTask).filter(DBGroupTask.group_task_id == group_task_id).first()
        if group_tasks:
            group_tasks_data : List[GroupTask] = [
            GroupTask(
            group_task_id=group_task.group_task_id,
            name=group_task.name,
            description=group_task.description,
            user_id=group_task.user_id,
            created_at=group_task.created_at,
            update_at=group_task.updated_at,           
            )
            for group_task in group_tasks
        ]
            return group_tasks_data
        else:
            return {"message": "Group task not found"}


@app.get("/group_tasks/{group_task_id}/tasks", tags=["GroupTask"], response_model=List[Task])
def get_group_tasks_tasks(group_task_id: int = Path(..., description="The ID of the Group tasks")) -> List[Task]:
   """
   Get tasks for a specific group task by group_task_id.

   """
   with session_scope(Session) as session:
        tasks = session.query(DBTask).filter(DBTask.group_task_id == group_task_id).all()
        if tasks:
            group_tasks_data : List[Task] = [
                GroupTask(
                    group_task_id=task.task_id,
                    name=task.task_id,
                    description=task.task_id,
                    user_id=task.task_id,
                    created_at=task.task_id,
                    updated_at=task.task_id,           
                )
            for  task in tasks
        ]
            return group_tasks_data
        else:
            return {"message": "Tasks for a specific group task by group_task_id not found"}


@app.get("/tasks", tags=["Task"], response_model=List[Task])
def get_tasks() -> List[Task]:
    """
    Get all tasks.
    """
    with session_scope(Session) as session:
        tasks = session.query(DBTask).all()
        if tasks:
            tasks_data : List[Task] = [
             Task(           
                task_id=task.task_id,
                name=task.name,
                iv_priority=task.iv_priority,
                period_ofexecution=task.period_ofexecution,
                group_task_id=task.group_task_id,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
                completed=task.completed                
            )
            for task in tasks
        ]
            return tasks_data
        else:
            return {"message": "Tasks not found"}


@app.get("/tasks/{task_id}", tags=["Task"], response_model=Task)
def get_task(task_id: int  = Path(..., description="The ID of the task")) -> Task:
    """
    Get a specific task by task_id.
    """
    with session_scope(Session) as session:
        task = session.query(DBTask).filter(Task.task_id == task_id).first()
        if task:
            tasks_data : Task = [
             Task(           
                task_id=tasks_data.task_id,
                name=tasks_data.name,
                iv_priority=tasks_data.iv_priority,
                period_ofexecution=tasks_data.period_ofexecution,
                group_task_id=tasks_data.group_task_id,
                user_id=tasks_data.user_id,
                created_at=tasks_data.created_at,
                updated_at=tasks_data.updated_at,
                completed=tasks_data.completed                
            )
            for group_task in task
        ]
            return tasks_data
        else:
            return {"message": "Task not found"}


@app.get("/tasks/{task_id}/user", tags=["Task"], response_model=List[User])
def get_task_users(task_id: int  = Path(..., description="The ID of the task")) -> List[User]:
    """
    Get user for a specific task by task_id.
    """
    with session_scope(Session) as session:
        users = session.query(DBUser).join(DBTask).filter(DBTask.task_id == task_id).all()
        if users:
            users_data = [
                User(
                    user_id=user.user_id,
                    name=user.name,
                    email=user.email,
                    password=user.password,
                    created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                )
                for user in users
            ]
            return users_data
        else:
            return {"message": "Task not found"}



@app.get("/comments", tags=["Comments"], response_model=List[Comment])
def get_comments() -> List[Comment]:
    """
    Get all comments.
    """
    with session_scope(Session) as session:
        comments = session.query(DBComment).all()
        if comments:
            comments_data = List[Comment] = [
            Comment(
            com_id=comment.com_id,
            text=comment.text,
            task_id=comment.task_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            user_id=comment.user_id,
            )        
            for comment in comments
        ]
            return comments_data
        else:
            return {"message": "Comments not found"}


@app.get("/comments/{comment_id}", tags=["Comments"], response_model=List[Comment])
def get_comment(comment_id: int = Path(..., description="The ID of comment")) -> List[Comment]:
    """
    Get a specific comment by comment_id.
    """
    with session_scope(Session) as session:
        comments = session.query(DBComment).filter(DBComment.com_id == comment_id).first()
        if comments:
            comments_data = List[Comment] = [
            Comment(
            com_id=comment.com_id,
            text=comment.text,
            task_id=comment.task_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            user_id=comment.user_id,
            )        
            for comment in comments
        ]
            return comments_data
        else:
            return {"message": "Comments not found"}


@app.get("/group_tasks/tasks", tags=["GroupTask"], response_model=List[Task])
def get_group_tasks_tasks() -> List[Task]:
    """
    Get all tasks from all group tasks.
    """
    with session_scope(Session) as session:
        tasks = session.query(DBTask).all()
        if tasks:
            tasks_data : Task = [
             Task(           
                task_id=task.task_id,
                name=task.name,
                iv_priority=task.iv_priority,
                period_ofexecution=task.period_ofexecution,
                group_task_id=task.group_task_id,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
                completed=task.completed                
            )
            for task in tasks
        ]
            return tasks_data
        else:
            return {"message": "Tasks not found"}


@app.get("/group_tasks/{group_task_id}/tasks/{task_id}", tags=["GroupTask"], response_model=List[Task])
async def get_group_task_task(group_task_id: int  = Path(..., description="The ID of Group tasks"), task_id: int  = Path(..., description="The ID of task")) -> List[Task]:
    """
    Get a specific task from a specific group task.
    """
    with session_scope(Session) as session:
        task = session.query(DBTask).filter_by(group_task_id=group_task_id, task_id=task_id).first()
        if task:
            tasks_data : Task = [
             Task(           
                task_id=task.task_id,
                name=task.name,
                iv_priority=task.iv_priority,
                period_ofexecution=task.period_ofexecution,
                group_task_id=task.group_task_id,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
                completed=task.completed                
            )
            for task in task
        ]
            return tasks_data
        else:
            return {"message": "Task not found"}


@app.get("/group_tasks/{group_task_id}/tasks/{task_id}/comments", tags=["GroupTask"], response_model=List[Comment])
async def get_group_task_task_comments(group_task_id: int = Path(..., description="The ID of Group tasks"), task_id: int = Path(..., description="The ID of task")) -> List[Comment]:
    """
    Get comments for a specific task in a specific group task.
    """
    with session_scope(Session) as session:
        comments = session.query(DBComment).filter(DBComment.task_id == task_id).all()
        if comments:
            comments_data = List[Comment] = [
            Comment(
            com_id=comment.com_id,
            text=comment.text,
            task_id=comment.task_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            user_id=comment.user_id,
            )        
            for comment in comments
        ]
            return comments_data
        else:
            return {"message": "Comments not found"}
