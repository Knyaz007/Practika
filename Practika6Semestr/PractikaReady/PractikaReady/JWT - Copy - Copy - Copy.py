from fastapi import Depends, FastAPI,Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from pydantic import BaseModel
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
# �������� ���� ������ SQLite
SQLALCHEMY_DATABASE_URL = "postgresql://student:1234@LocalHost:5432/practika"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    return db



# ������ ������������
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)


Base.metadata.create_all(bind=engine)

app = FastAPI()

# ����������� ����������� ����������
app.mount("/static", StaticFiles(directory="static"), name="static")

# ����������� ������������� Jinja2
 
templates = Jinja2Templates(directory="static/templates")

# ������������ �������������� � �������������� JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# ��������� access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #print("Access Token:", encoded_jwt)  # �������� ��� ������
    return encoded_jwt


# ��������� ������������ �� email �� ���� ������
def get_user(email: str, db: SessionLocal):
    return db.query(User).filter(User.email == email).first()


# ��������� �������� ������������ �� ������ ������ �������
async def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    #print("Received Token:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        user = get_user(email, db)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


# ������ ������� ��� �������������� ������������
class UserLoginRequest(BaseModel):
    email: str
    password: str


# ������ ������ �� ������� �������������
class UserResponse(BaseModel):
    id: int
    email: str


# ���� ��� ��������� ������ ������� (��������������)
@app.post("/token")
async def login(user_login: UserLoginRequest, db: SessionLocal = Depends(get_db)):
    #print("Received Login Request")
    #print("Username:", user_login.email)
    #print("Password:", user_login.password)
    
    user = get_user(user_login.email, db)
    if user is None or not user.verify_password(user_login.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}



#��� ���������� ������, ��� �� ������� � ��������� authorization: str = Header(...) ���� ..., ��� 
#��������, ��� ��������� authorization ���������� � ������ �������������� � �������.

from fastapi import Header
## ���� ��� ��������� ������ �������������

from fastapi.security import HTTPBearer
http_bearer = HTTPBearer()
























import logging

# ��������� �������
logging.basicConfig(level=logging.INFO)

# ����������� �������
def log_request(request):
    logger = logging.getLogger(__name__)
    logger.info("Request: %s %s", request.method, request.url)
    for header, value in request.headers.items():
        logger.info("%s: %s", header, value)


@app.get("/users", response_model=List[UserResponse])
async def get_users(request: Request, authorization: str = Header(None)):

    if authorization is None:
        # ��������� ���������� ��������� �����������
        # ��������, �� �������� ������� ������ ��� ��������� ������ ��������
         users2 = [
        UserResponse(id=6, email="example1@example.com"),
        UserResponse(id=5, email="example2@example.com"),
        UserResponse(id=4, email="example3@example.com"),
        UserResponse(id=3, email="example3@example.com"),
        UserResponse(id=3, email="example3@example.com"),
        UserResponse(id=3, email="example3@example.com")
    ]
         return users2
    # ��������� ������� � ��������� �����������
    # ����� �� ������ ������������ �������� authorization ��� ���������� ���������
    print(f"Authorization header: {authorization}")

    # ������ � ������ ����������
    headers = request.headers
    print(f"Headers: {headers}")

    # ������ � ������ ��������� �������
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Client host: {request.client.host}")
    #log_request(request)  # ����������� �������

    access_token = authorization.split("Bearer ")[-1]    # ���������� ������ �� ��������� �����������
    # ����� �� ������ ������������ ����� ��� �������� ������� � ������ �������������
    users = [
        UserResponse(id=1, email="example1@example.com"),
        UserResponse(id=2, email="example2@example.com"),
        UserResponse(id=3, email="example3@example.com"),
    ]
    #return users
    return users

#@app.get("/users", response_model=List[UserResponse])
#async def get_users(current_user: User = Depends(get_current_user)):
#    db = get_db()

#    users = [
#        UserResponse(id=1, email="example1@example.com"),
#        UserResponse(id=2, email="example2@example.com"),
#        UserResponse(id=3, email="example3@example.com"),
#    ]
#    #users = db.query(User).all()
#    return users
#    #return [UserResponse(id=user.id, email=user.email) for user in users]


# ���� ��� ����������� �������� ��������������
@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login3.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
