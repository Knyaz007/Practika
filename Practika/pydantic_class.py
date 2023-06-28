from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    user_id: int
    name: str
    email: str
    password: str


class GroupTask(BaseModel):
    group_task_id: int
    name: str
    description: str
    user_id: int


class Task(BaseModel):
    task_id: int
    name: str
    iv_priority: int
    period_ofexecution: datetime
    group_task_id: int
    user_id: int


class Comment(BaseModel):
    com_id: int
    text: str
    task_id: int
