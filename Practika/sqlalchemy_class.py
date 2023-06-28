from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import List, Optional

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(255))
    email: str = Column(String(255))
    password: str = Column(String(255))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    group_tasks: List["GroupTask"] = relationship("GroupTask", back_populates="user")
    tasks: List["Task"] = relationship("Task", back_populates="user")
    comments: List["Comment"] = relationship("Comment", back_populates="user")


class GroupTask(Base):
    __tablename__ = "group_tasks"

    group_task_id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(255))
    description: Optional[str] = Column(Text)
    user_id: int = Column(Integer, ForeignKey("users.user_id"))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Optional[User] = relationship("User", back_populates="group_tasks")
    tasks: List["Task"] = relationship("Task", back_populates="group_task")


class Task(Base):
    __tablename__ = "tasks"

    task_id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(255))
    iv_priority: Optional[int] = Column(Integer)
    period_ofexecution: Optional[Date] = Column(Date)
    group_task_id: int = Column(Integer, ForeignKey("group_tasks.group_task_id"))
    user_id: int = Column(Integer, ForeignKey("users.user_id"))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Optional[User] = relationship("User", back_populates="tasks")
    group_task: Optional[GroupTask] = relationship("GroupTask", back_populates="tasks")
    comments: List["Comment"] = relationship("Comment", back_populates="task")


class Comment(Base):
    __tablename__ = "comments"

    com_id: int = Column(Integer, primary_key=True, autoincrement=True)
    text: str = Column(Text)
    task_id: int = Column(Integer, ForeignKey("tasks.task_id"))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id: int = Column(Integer, ForeignKey("users.user_id"))

    user: Optional[User] = relationship("User", back_populates="comments")
    task: Optional[Task] = relationship("Task", back_populates="comments")

