import pytest
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

# Users
def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    users_data = response.json()  
    assert len(users_data) >= 1, "Not an empty list of users was expected"
   
test_get_users()

def test_get_user_id():
    response = client.get("/users/1")
    users_data = response.json()
    assert response.status_code == 200
    expected_user = [
        {"id": 1, "name": "vvv", "created_at": "1997-02-12 00:00:00"},
        
    ]
    # Рeшил просто вывести что нету польщователя нежели проверять его с моим 
    if not users_data:
        assert False, "User not found"    
        
test_get_user_id()

def test_get_user_id_task():
    response = client.get("/users/1/tasks")
    task_data = response.json()
    assert response.status_code == 200   
    if not task_data:
        assert False, "User not found"

test_get_user_id_task()

def test_get_user_id_group_tasks():
    response = client.get("/users/1/group_tasks")
    task_data = response.json()
    assert response.status_code == 200   
    if not task_data:
        assert False, "Group tasks not found"

test_get_user_id_group_tasks()

def test_get_user_id_comments():
    user_id = 1
    response = client.get(f"/users/{user_id}/comments")
    assert response.status_code == 200
    comments = response.json()
    if not comments:
        assert False, "Comments tasks not found"

test_get_user_id_comments()


# ------------------------------------  Группы задач (GroupTask) ---------------------------------------
def test_get_group_tasks():
    response = client.get("/group_tasks")
    group_tasks = response.json()
    tr = len(group_tasks)
    assert len(group_tasks) >= 1, "Not an empty list of group_tasks was expected"
   
test_get_group_tasks()

def test_get_group_task_group_task_id():
    group_task_id = 1
    response = client.get(f"/group_tasks/{group_task_id}/")
    group_task = response.json()
    assert response.status_code == 200
    #assert response.json() == {"id": 1, "name": "one", "created_at": "2000-11-11 00:00:00"}
    if not group_task:
        assert False, "Group task not found"

test_get_group_task_group_task_id()

def test_get_group_task_group_task_id_tasks():
    group_task_id = 1
    response = client.get(f"/group_tasks/{group_task_id}/tasks")
    group_task = response.json()
    assert response.status_code == 200
    #assert response.json() == {"id": 1, "name": "one", "created_at": "2000-11-11 00:00:00"}
    if not group_task:
        assert False, "Group task not found"

test_get_group_task_group_task_id_tasks()

# Задачи (Task)
def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    if not tasks:
        assert False, "Tasks not found"

test_get_tasks()

def test_get_task():
    response = client.get("/tasks/1")
    task = response.json()
    assert response.status_code == 200, "status code is not 200"
    if not task:
        assert False, "Task not found"
   
test_get_tasks()

def test_get_tasks_id_user():
    response = client.get("/tasks/1/user")
    task = response.json()
    assert response.status_code == 200 , "status code is not 200"
    if not task:
        assert False, "Task not found"
   
test_get_tasks_id_user()

# Comments
def test_get_comments():
    response = client.get("/comments")
    comments = response.json()
    assert response.status_code == 200
    if not comments:
        assert False, "Comments not found"

test_get_comments()


def test_get_comment_id():
    response = client.get("/comments/1")
    assert response.status_code == 200
    comments = response.json()
    if not comments:
        assert False, "ID comment not found"

test_get_comment_id()

# ------------------------  Группы задач и их связи с задачами и комментариями  -------------------------------------

def test_get_group_tasks_tasks():
    response = client.get("/group_tasks/tasks")
    group_tasks = response.json()
    assert response.status_code == 200 , "status code is not 200"
    if not group_tasks:
        assert False, "Group tasks not found"

test_get_group_tasks_tasks()

def test_get_group_task_group_task_id_task_task_id():
    response = client.get("/group_tasks/1/tasks/1")
    group_tasks = response.json()
    assert response.status_code == 200, "Expected status code 200"
    if not group_tasks:
        assert False, "Group tasks not found" 

test_get_group_task_group_task_id_task_task_id()


def get_group_task_group_task_id_task_task_id_comments():
    response = client.get("/group_tasks/1/tasks/1/comments")
    group_tasks = response.json()
    assert response.status_code == 200, "Expected status code 200"
    if not group_tasks:
        assert False, "Comments not found"

get_group_task_group_task_id_task_task_id_comments()


## Run the tests
#if __name__ == "__main__":
#    pytest.main()
