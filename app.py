from fastapi import FastAPI
from database import Database
from models import Product, User

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

@app.get("/product")
def get_product():
    session = database.get_session()
    example = session.query(Product).all()
    if example == []:
        return {"message": "no data"}
    print(example)
    session.close()
    return example

@app.post("/donation/upload")
def upload_donation(user_id: int, Product_Title: str, Prodcut_description: str, brandName: str, dateOfManufacture: str, color: str, category: str):
    session = database.get_session()
    user = session.query(User).filter(User.id == user_id).first()
    if user == None:
        return {"status": "user not found"}
    else:
        product = Product(title=Product_Title, description=Prodcut_description, brand_name=brandName, date_of_manufacture=dateOfManufacture, color=color, category=category)
        session.add(product)
        session.commit()
        session.close()
        return {"status": "success"}