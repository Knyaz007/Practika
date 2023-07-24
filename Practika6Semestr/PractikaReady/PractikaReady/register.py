# -*- coding: utf-8 -*- 
# ��� �������� ����� 
from fastapi import FastAPI, Depends , Request, Form
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from pydantic import BaseModel
import uvicorn
from fastapi.templating import Jinja2Templates

from passlib.context import CryptContext #����������� 

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

 



SQLALCHEMY_DATABASE_URL = "postgresql://student:1234@LocalHost:5432/practika"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



Base.metadata.create_all(bind=engine)

app = FastAPI()

# ����������� ����������� ����������
app.mount("/static", StaticFiles(directory="static"), name="static")

# ����������� ������������� Jinja2
templates = Jinja2Templates(directory="static/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  #�����������


#������ Pydantic
def get_db():
   
    db = SessionLocal()
   
    try:
        yield db
    finally:
        db.close()




@app.get("/")
def read_root():
    return {"Hello": "World"}

#������ SQLAlchemy ��� ����������� �������������
class Registration(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String)

#������ Pydantic ��� ����������� �������������
class RegistrationRequest(BaseModel):
    name: str
    email: str
    password: str






# Form(...) ��� ������� ������ ������ ���� ���������� ��� ������ �����
@app.post("/register")
async def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db=Depends(get_db)):
     # ���������, ��� ������������ � ����� �� ����������� ������ ��� �� ���������������
    user = db.query(Registration).filter(Registration.email == email).first() #email �� ���� �����
    if user:
        return {"error": "User with this email already exists"}

     # ������� ������ ������������
     # ����������� ������ ��� �����������
    hashed_password = pwd_context.hash(password)
    new_user = Registration(name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"Dobavleno! "}

@app.get("/registration-form")
async def registration_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.get("/login-form")
async def registration_form(request: Request):
    return templates.TemplateResponse("Authentication.html", {"request": request})

# ������� ��������������
@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...), db=Depends(get_db)):
    # ����� ������������ � ���� ������ �� ����������� �����
    user = db.query(Registration).filter(Registration.email == email).first()
    if not user:
        return {"message": "Invalid email or password"}

    # �������� ������
     #�������� ������ ��� ��������������
    if not pwd_context.verify(password, user.password):
        return {"message": "Invalid email or password"}
    return {"access_token": email, "token_type": "bearer"}
    #return {"message": "Login successful"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
