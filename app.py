from fastapi import FastAPI
from database import Database
from models import Test

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

@app.post("/create")
async def create(name: str, number: int):
    session = database.get_session()
    test = Test(name=name, number=number)
    session.add(test)
    session.commit()
    session.close()
    return {"message": "created"}

@app.delete("/delete/{id}")
async def delete(id: int):
    session = database.get_session()
    session.query(Test).filter(Test.id == id).delete()
    session.commit()
    session.close()
    return {"message": "deleted"}

@app.put("/update/{id}")
async def update(id: int, name: str, number: int):
    session = database.get_session()
    session.query(Test).filter(Test.id == id).update({"name": name, "number": number})
    session.commit()
    session.close()
    return {"message": "updated"}

@app.get("/get/{id}")
async def get(id: int):
    session = database.get_session()
    example = session.query(Test).filter(Test.id == id).first()
    if example == None:
        return {"message": "no data"}
    session.close()
    return example

@app.get("/get_by_name/{name}")
async def get_by_name(name: str):
    session = database.get_session()
    example = session.query(Test).filter(Test.name == name).all()
    if example == []:
        return {"message": "no data"}
    session.close()
    return example

@app.get("/get_by_number/{number}")
async def get_by_number(number: int):
    session = database.get_session()
    example = session.query(Test).filter(Test.number == number).all()
    if example == []:
        return {"message": "no data"}
    session.close()
    return example