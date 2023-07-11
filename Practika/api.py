# -*- coding: windows-1251 -*-
from fastapi import FastAPI, Path
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

# ������� ���������� � ����� ������
engine = create_engine(db.original_location)
Session = sessionmaker(bind=engine)


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


# ���������� ���� ���� � �������� �����

# ������� ��� ��������� Swagger-�����
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


# ������� ��� ��������� Swagger-�����
@app.get("/openapi.json")
async def get_openapi_endpoint():
    return custom_openapi()


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
                    updated_at=db_user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                )
                for db_user in db_users
            ]
            return users_data


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
                updated_at=db_user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            )
            return user_data


@app.post("/users", tags=["Users"])
async def create_user():
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


@app.get("/users/{user_id}/tasks", tags=["Users"], response_model=List[Task])
def get_user_tasks(user_id: int = Path(..., description="The ID of the user")) -> List[Task]:
    """
    Get tasks for a specific user by user_id.
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
                    created_at=db_task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=db_task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    completed=db_task.completed
                )
                for db_task in db_tasks
            ]
            return tasks_data


@app.get("/users/{user_id}/group_tasks", tags=["Users"], response_model=List[GroupTask])
def get_user_group_tasks(user_id: int = Path(..., description="The ID of the user")) -> List[GroupTask]:
    """
    Get group tasks for a specific user by user_id.
    """
    with session_scope(Session) as session:
        group_tasks = session.query(DBGroupTask).filter(DBGroupTask.user_id == user_id).all()
        if group_tasks:
            group_tasks_data: List[GroupTask] = [
                GroupTask(
                    group_task_id=group_task.group_task_id,
                    name=group_task.name,
                    description=group_task.description,
                    user_id=group_task.user_id,
                    created_at=group_task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=group_task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                )
                for group_task in group_tasks
            ]
            return group_tasks_data


@app.get("/users/{user_id}/comments", tags=["Users"], response_model=List[Comment])
def get_user_comments(user_id: int = Path(..., description="The ID of the user")) -> List[Comment]:
    """
    Get comments for a specific user by user_id.
    """
    with session_scope(Session) as session:
        comments = session.query(DBComment).filter(DBComment.user_id == user_id).all()
        if comments:
            comments_data: List[Comment] = [
                Comment(
                    com_id=comment.com_id,
                    text=comment.text,
                    task_id=comment.task_id,
                    created_at=comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=comment.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    user_id=comment.user_id,
                )
                for comment in comments
            ]
            return comments_data


@app.get("/group_tasks", tags=["GroupTask"], response_model=List[GroupTask])
def get_group_tasks() -> List[GroupTask]:
    """
    Get all group tasks.
    """
    with session_scope(Session) as session:
        group_tasks = session.query(DBGroupTask).all()
        if group_tasks:
            group_tasks_data: List[GroupTask] = [
                GroupTask(
                    group_task_id=group_task.group_task_id,
                    name=group_task.name,
                    description=group_task.description,
                    user_id=group_task.user_id,
                    created_at=group_task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=group_task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                )
                for group_task in group_tasks
            ]
            return group_tasks_data
        else:
            return group_tasks


@app.get("/group_tasks/{group_task_id}", tags=["GroupTask"], response_model=GroupTask)
def get_group_task(group_task_id: int = Path(..., description="The ID of the Group tasks")) -> GroupTask:
    """
    Get a specific group task by group_task_id.
    """
    with session_scope(Session) as session:
        group_task = session.query(DBGroupTask).filter(DBGroupTask.group_task_id == group_task_id).first()
        if group_task:
            group_tasks_data = GroupTask(
                group_task_id=group_task.group_task_id,
                name=group_task.name,
                description=group_task.description,
                user_id=group_task.user_id,
                created_at=group_task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=group_task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            )
            return group_tasks_data


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


@app.get("/group_tasks/{group_task_id}/tasks", tags=["GroupTask"], response_model=List[Task])
def get_group_tasks_tasks(group_task_id: int = Path(..., description="The ID of the Group tasks")) -> List[Task]:
    """
    Get tasks for a specific group task by group_task_id.
    """
    with session_scope(Session) as session:
        tasks = session.query(DBTask).filter(DBTask.group_task_id == group_task_id).all()
        if tasks:
            tasks_data: List[Task] = [
                Task(
                    task_id=task.task_id,
                    name=task.name,
                    iv_priority=task.iv_priority,
                    period_ofexecution=task.period_ofexecution.strftime("%Y-%m-%d %H:%M:%S"),
                    group_task_id=task.group_task_id,
                    user_id=task.user_id,
                    created_at=task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                )
                for task in tasks
            ]
            return tasks_data


@app.get("/tasks", tags=["Task"], response_model=List[Task])
def get_tasks() -> List[Task]:
    """
    Get all tasks.
    """
    with session_scope(Session) as session:
        tasks = session.query(DBTask).all()
        if tasks:
            tasks_data: List[Task] = [
                Task(
                    task_id=task.task_id,
                    name=task.name,
                    iv_priority=task.iv_priority,
                    period_ofexecution=task.period_ofexecution.strftime("%Y-%m-%d %H:%M:%S"),
                    group_task_id=task.group_task_id,
                    user_id=task.user_id,
                    created_at=task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    completed=task.completed,
                )
                for task in tasks
            ]
            return tasks_data
        else:
            return tasks


@app.get("/tasks/{task_id}", tags=["Task"], response_model=Task)
def get_task(task_id: int = Path(..., description="The ID of the task")) -> Task:
    """
    Get a specific task by task_id.
    """
    with session_scope(Session) as session:
        task = session.query(DBTask).filter(DBTask.task_id == task_id).first()
        if task:
            tasks_data = Task(
                task_id=task.task_id,
                name=task.name,
                iv_priority=task.iv_priority,
                period_ofexecution=task.period_ofexecution.strftime("%Y-%m-%d %H:%M:%S"),
                group_task_id=task.group_task_id,
                user_id=task.user_id,
                created_at=task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                completed=task.completed,
            )
            return tasks_data


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


@app.get("/tasks/{task_id}/user", tags=["Task"], response_model=List[User])
def get_task_users(task_id: int = Path(..., description="The ID of the task")) -> List[User]:
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
                    updated_at=user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                )
                for user in users
            ]
            return users_data


# --------------------------------------------- ����������� (Comments) --------------------------------------------

@app.get("/comments", tags=["Comments"], response_model=List[Comment])
def get_comments() -> List[Comment]:
    """
    Get all comments.
    """
    with session_scope(Session) as session:
        comments = session.query(DBComment).all()
        if comments:
            comments_data: List[Comment] = [
                Comment(
                    com_id=comment.com_id,
                    text=comment.text,
                    task_id=comment.task_id,
                    created_at=comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=comment.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    user_id=comment.user_id,
                )
                for comment in comments
            ]
            return comments_data
        else:
            return comments


@app.get("/comments/{comment_id}", tags=["Comments"], response_model=Comment)
def get_comment(comment_id: int = Path(..., description="The ID of comment")) -> Comment:
    """
    Get a specific comment by comment_id.
    """
    with session_scope(Session) as session:
        comments = session.query(DBComment).filter(DBComment.com_id == comment_id).first()
        if comments:
            comment_data = Comment(
                com_id=comments.com_id,
                text=comments.text,
                task_id=comments.task_id,
                created_at=comments.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=comments.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                user_id=comments.user_id,
            )
            return comment_data


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


# ------------------------  ������ ����� � �� ����� � �������� � �������������  -------------------------------------

@app.get("/group_tasks/tasks/", tags=["GroupTask"], response_model=List[Task])
def get_group_tasks_tasks() -> List[Task]:
    """
    Get all tasks from all group tasks.
    """
    with session_scope(Session) as session:
        tasks = session.query(DBTask).all()
        if tasks:
            tasks_data: List[Task] = [
                Task(
                    task_id=task.task_id,
                    name=task.name,
                    iv_priority=task.iv_priority,
                    period_ofexecution=task.period_ofexecution.strftime("%Y-%m-%d %H:%M:%S"),
                    group_task_id=task.group_task_id,
                    user_id=task.user_id,
                    created_at=task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                )
                for task in tasks
            ]
            return tasks_data


@app.get("/group_tasks/{group_task_id}/tasks/{task_id}", tags=["GroupTask"], response_model=Task)
async def get_group_task_task(
    group_task_id: int = Path(..., description="The ID of Group tasks"),
    task_id: int = Path(..., description="The ID of task"),
) -> Task:
    """
    Get a specific task from a specific group task.
    """
    with session_scope(Session) as session:
        task = (
            session.query(DBTask)
            .filter_by(group_task_id=group_task_id, task_id=task_id)
            .first()
        )
        if task:
            tasks_data = Task(
                task_id=task.task_id,
                name=task.name,
                iv_priority=task.iv_priority,
                period_ofexecution=task.period_ofexecution.strftime("%Y-%m-%d %H:%M:%S"),
                group_task_id=task.group_task_id,
                user_id=task.user_id,
                created_at=task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=task.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            )
            return tasks_data


@app.get(
    "/group_tasks/{group_task_id}/tasks/{task_id}/comments",
    tags=["GroupTask"],
    response_model=List[Comment],
)
async def get_group_task_task_comments(
    group_task_id: int = Path(..., description="The ID of Group tasks"),
    task_id: int = Path(..., description="The ID of task"),
) -> List[Comment]:
    """
    Get comments for a specific task in a specific group task.
    """
    with session_scope(Session) as session:
        comments = session.query(DBComment).filter(DBComment.task_id == task_id).all()
        if comments:
            comments_data: List[Comment] = [
                Comment(
                    com_id=comment.com_id,
                    text=comment.text,
                    task_id=comment.task_id,
                    created_at=comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=comment.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    user_id=comment.user_id,
                )
                for comment in comments
            ]
            return comments_data
        else:
            return comments
