from sqlalchemy import Column, Integer, String, DateTime, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(255))
    email: Mapped[str] = Column(String(255))
    password: Mapped[str] = Column(String(255))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    group_tasks: Mapped[List["GroupTask"]] = relationship("GroupTask", back_populates="user")
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")


class GroupTask(Base):
    __tablename__ = "group_tasks"

    group_task_id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(255))
    description: Mapped[Optional[str]] = Column(Text)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.user_id"))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[Optional[User]] = relationship("User", back_populates="group_tasks")
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="group_task")


class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(255))
    iv_priority: Mapped[Optional[int]] = Column(Integer)
    period_ofexecution: Mapped[Optional[Date]] = Column(Date)
    group_task_id: Mapped[int] = Column(Integer, ForeignKey("group_tasks.group_task_id"))
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.user_id"))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed: Mapped[bool] = Column(Boolean, default=False)

    user: Mapped[Optional[User]] = relationship("User", back_populates="tasks")
    group_task: Mapped[Optional[GroupTask]] = relationship("GroupTask", back_populates="tasks")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="task")


class Comment(Base):
    __tablename__ = "comments"

    com_id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = Column(Text)
    task_id: Mapped[int] = Column(Integer, ForeignKey("tasks.task_id"))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id: Mapped[int] = Column(Integer, ForeignKey("users.user_id"))

    user: Mapped[Optional[User]] = relationship("User", back_populates="comments")
    task: Mapped[Optional[Task]] = relationship("Task", back_populates="comments")
