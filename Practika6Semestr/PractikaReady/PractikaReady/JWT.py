from fastapi import Depends, FastAPI, HTTPException, Request, Form
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

SQLALCHEMY_DATABASE_URL = "postgresql://student:1234@LocalHost:5432/practika"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    #phone = Column(String, index=True)
    #address = Column(String)
    password = Column(String)


    def update_email(self, new_email: str):
        self.email = new_email


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключение статической директории
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение шаблонизатора Jinja2
templates = Jinja2Templates(directory="static/templates")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    #phone: int
    #address: str

    #модель SQLAlchemy для регистрации пользователей




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_id(db: SessionLocal, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


# Конфигурация аутентификации с использованием JWT

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Генерация access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Проверка хэша пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Получение пользователя по email из базы данных
def get_user(email: str, db: SessionLocal):
    return db.query(User).filter(User.email == email).first()

 
from fastapi.responses import RedirectResponse 

# Маршрут для генерации токена доступа (аутентификации)
@app.post("/token")
async def login(request: Request,form_data: OAuth2PasswordRequestForm = Depends()):
    print("/token",form_data)
    #print("/form_data.body()", form_data.body())
    db = next(get_db())
    user = get_user(form_data.username, db)
    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    #return RedirectResponse(url="/users")
    ##print("/oauth2_scheme",access_token)
    return templates.TemplateResponse("login.html", {"request": request, "access_token": access_token})




# Получение текущего пользователя на основе токена доступа
async def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    print("/get_current_user-token---",token)
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

   
@app.get("/users", response_model=List[UserResponse])
async def get_users(current_user: User = Depends(get_current_user),db=Depends(get_db)):
    users = db.query(User).all()
    #return [UserResponse(id=user.id, name=user.name, email=user.email, phone=user.phone, address=user.address) for user in users]
    return [UserResponse(id=user.id, name=user.name, email=user.email) for user in users]




@app.get("/login-form")
async def registration_form(request: Request):
    return templates.TemplateResponse("Authentication2.html", {"request": request})
    



#@app.get("/users", response_model=List[UserResponse])
#async def get_users(current_user: User = Depends(get_current_user), db=Depends(get_db)):
#    users = db.query(User).all()
#    return [
#        UserResponse(id=user.id, name=user.name, email=user.email, phone=user.phone, address=user.address)
#        for user in users
#    ]

 
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
