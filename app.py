from fastapi import FastAPI
from database import Database
from models import Test
from models import User

app = FastAPI()

database = Database()

@app.get("/")
async def root():
    session = database.get_session()
    example = session.query(Test).all()
    if example == []:
        return {"message": "no data"}
    print(example)
    session.close()
    return example

@app.get("/user")
def get_user():
    session = database.get_session()
    example = session.query(User).all()
    if example == []:
        return {"message": "no data"}
    print(example)
    session.close()
    return example

@app.post("/user")
def create_user(name: str, email: str, password: str, phonenumber: str):
    session = database.get_session()
    user = User(name=name, email=email, password=password, phonenumber=phonenumber)
    session.add(user)
    session.commit()
    session.close()
    return {"message": "success"}