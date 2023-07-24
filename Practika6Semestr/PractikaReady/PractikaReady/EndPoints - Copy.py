#без типизации

from fastapi import FastAPI
from typing import Dict

app = FastAPI()

# Пользователи (Users)
@app.get("/users")
async def get_users() -> Dict[str, str]:
    return {"message": "Get all users"}

@app.get("/users/{user_id}")
async def get_user(user_id: int) -> Dict[str, str]:
    return {"message": f"Get user {user_id}"}

@app.post("/users")
async def create_user() -> Dict[str, str]:
    return {"message": "Create a new user"}

@app.put("/users/{user_id}")
async def update_user(user_id: int) -> Dict[str, str]:
    return {"message": f"Update user {user_id}"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int) -> Dict[str, str]:
    return {"message": f"Delete user {user_id}"}

@app.get("/users/{user_id}/tasks")
async def get_user_tasks(user_id: int) -> Dict[str, str]:
    return {"message": f"Get tasks for user {user_id}"}

@app.get("/users/{user_id}/group_tasks")
async def get_user_group_tasks(user_id: int) -> Dict[str, str]:
    return {"message": f"Get group tasks for user {user_id}"}

@app.get("/users/{user_id}/completed_tasks")
async def get_user_completed_tasks(user_id: int) -> Dict[str, str]:
    return {"message": f"Get completed tasks for user {user_id}"}

@app.get("/users/{user_id}/comments")
async def get_user_comments(user_id: int) -> Dict[str, str]:
    return {"message": f"Get comments for user {user_id}"}


# Группы задач (GroupTask)
@app.get("/group_tasks")
async def get_group_tasks() -> Dict[str, str]:
    return {"message": "Get all group tasks"}

@app.get("/group_tasks/{group_task_id}")
async def get_group_task(group_task_id: int) -> Dict[str, str]:
    return {"message": f"Get group task {group_task_id}"}

@app.post("/group_tasks")
async def create_group_task() -> Dict[str, str]:
    return {"message": "Create a new group task"}

@app.put("/group_tasks/{group_task_id}")
async def update_group_task(group_task_id: int) -> Dict[str, str]:
    return {"message": f"Update group task {group_task_id}"}

@app.delete("/group_tasks/{group_task_id}")
async def delete_group_task(group_task_id: int) -> Dict[str, str]:
    return {"message": f"Delete group task {group_task_id}"}

@app.get("/group_tasks/{group_task_id}/tasks")
async def get_group_tasks_tasks(group_task_id: int) -> Dict[str, str]:
    return {"message": f"Get tasks for group task {group_task_id}"}


# Задачи (Task)
@app.get("/tasks")
async def get_tasks() -> Dict[str, str]:
    return {"message": "Get all tasks"}

@app.get("/tasks/{task_id}")
async def get_task(task_id: int) -> Dict[str, str]:
    return {"message": f"Get task {task_id}"}

@app.post("/tasks")
async def create_task() -> Dict[str, str]:
    return {"message": "Create a new task"}

@app.put("/tasks/{task_id}")
async def update_task(task_id: int) -> Dict[str, str]:
    return {"message": f"Update task {task_id}"}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int) -> Dict[str, str]:
    return {"message": f"Delete task {task_id}"}

@app.get("/tasks/{task_id}/users")
async def get_task_users(task_id: int) -> Dict[str, str]:
    return {"message": f"Get users for task {task_id}"}


# Комментарии (Comments)
@app.get("/comments")
async def get_comments() -> Dict[str, str]:
    return {"message": "Get all comments"}

@app.get("/comments/{comment_id}")
async def get_comment(comment_id: int) -> Dict[str, str]:
    return {"message": f"Get comment {comment_id}"}

@app.post("/comments")
async def create_comment() -> Dict[str, str]:
    return {"message": "Create a new comment"}

@app.put("/comments/{comment_id}")
async def update_comment(comment_id: int) -> Dict[str, str]:
    return {"message": f"Update comment {comment_id}"}

@app.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int) -> Dict[str, str]:
    return {"message": f"Delete comment {comment_id}"}


# Группы задач и их связи с задачами и комментариями
@app.get("/group_tasks/tasks")
async def get_group_tasks_tasks() -> Dict[str, str]:
    return {"message": "Get all tasks from all group tasks"}

@app.get("/group_tasks/{group_task_id}/tasks")
async def get_group_task_tasks(group_task_id: int) -> Dict[str, str]:
    return {"message": f"Get tasks for group task {group_task_id}"}

@app.get("/group_tasks/{group_task_id}/tasks/{task_id}")
async def get_group_task_task(group_task_id: int, task_id: int) -> Dict[str, str]:
    return {"message": f"Get task {task_id} from group task {group_task_id}"}

@app.get("/group_tasks/{group_task_id}/tasks/{task_id}/comments")
async def get_group_task_task_comments(group_task_id: int, task_id: int) -> Dict[str, str]:
    return {"message": f"Get comments for task {task_id} in group task {group_task_id}"}
