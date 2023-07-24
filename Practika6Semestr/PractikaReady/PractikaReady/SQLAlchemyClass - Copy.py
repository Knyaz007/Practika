#без типизации
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    group_tasks = relationship("GroupTask", back_populates="user")
    tasks = relationship("Task", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class GroupTask(Base):
    __tablename__ = "group_tasks"

    group_task_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="group_tasks")
    tasks = relationship("Task", back_populates="group_task")


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    iv_priority = Column(Integer)
    period_ofexecution = Column(Date)
    group_task_id = Column(Integer, ForeignKey("group_tasks.group_task_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="tasks")
    group_task = relationship("GroupTask", back_populates="tasks")
    comments = relationship("Comment", back_populates="task")


class Comment(Base):
    __tablename__ = "comments"

    com_id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text)
    task_id = Column(Integer, ForeignKey("tasks.task_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="comments")
    task = relationship("Task", back_populates="comments")


