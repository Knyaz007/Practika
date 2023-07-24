from fastapi import FastAPI, Depends , Request, Form
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from pydantic import BaseModel
import uvicorn
from fastapi.templating import Jinja2Templates


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

 



SQLALCHEMY_DATABASE_URL = "postgresql://student:1234@LocalHost:5432/practika"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#модель SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    address = Column(String)

    def update_email(self, new_email: str):
        self.email = new_email


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключение статической директории
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение шаблонизатора Jinja2
templates = Jinja2Templates(directory="static/templates")
#модель Pydantic
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: int
    address: str


def get_db():
   
    db = SessionLocal()
   
    try:
        yield db
    finally:
        db.close()


def get_user_by_id(db: SessionLocal, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users", response_model=List[UserResponse])
async def get_users(db=Depends(get_db)):
    users = db.query(User).all()
    return [UserResponse(id=user.id, name=user.name, email=user.email, phone=user.phone, address=user.address) for user in users]


#@app.put("/users/{user_id}/email")
#async def update_user_email(user_id: int, email: str, db=Depends(get_db)):
#    user = get_user_by_id(db, user_id)
#    if not user:
#        return {"error": "User not found"}

#    user.update_email(email)
#    db.commit()

#    return user
@app.put("/users/{user_id}/email")
async def update_user_email(user_id: int, email: str, request: Request, db=Depends(get_db)):
    # остальной код

    print(await request.body())
    user = get_user_by_id(db, user_id)
    if not user:
        return {"error": "User not found"}

    user.update_email(email)
    db.commit()

    return user



@app.get("/update-email")
async def update_email(request: Request):
    return templates.TemplateResponse("update_email.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
