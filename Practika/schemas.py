from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    user_id: int
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime


class NewUser(BaseModel):   
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime


class GroupTask(BaseModel):
    group_task_id: int
    name: str
    description: str
    user_id: int
    created_at: datetime
    updated_at: datetime


class NewGroupTask(BaseModel):
    name: str
    description: str
    user_id: int
    created_at: datetime
    updated_at: datetime


class Task(BaseModel):
    task_id: int
    name: str
    iv_priority: int
    period_ofexecution: datetime
    group_task_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class NewTask(BaseModel):
    name: str
    iv_priority: int
    period_ofexecution: datetime
    group_task_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class Comment(BaseModel):
    com_id: int
    text: str
    task_id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

class NewComment(BaseModel):
    text: str
    task_id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
