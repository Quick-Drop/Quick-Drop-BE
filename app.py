from fastapi import FastAPI
from database import Database
from models import User

app = FastAPI()

database = Database()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

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

@app.delete("/user")
def delete_user(id: int):
    session = database.get_session()
    user = session.query(User).filter(User.id == id).first()
    session.delete(user)
    session.commit()
    session.close()
    return {"message": "success"}