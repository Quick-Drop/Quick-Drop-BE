from fastapi import FastAPI
from database import Database
from models import Product, User
from pydantic import BaseModel

app = FastAPI()

database = Database()

class UserRequest(BaseModel):
    name: str
    email: str
    password: str
    phonenumber: str

class ProductRequest(BaseModel):
    user_id: int
    Product_Title: str
    Product_description: str
    brandName: str
    dateOfManufacture: str
    color: str
    category: str

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
def create_user(user_request: UserRequest):
    session = database.get_session()
    user = User(
        name=user_request.name,
        email=user_request.email,
        password=user_request.password,
        phonenumber=user_request.phonenumber
    )
    session.add(user)
    session.commit()
    session.close()
    return {"status": "success"}

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
def create_product(product_request: ProductRequest):
    session = database.get_session()
    user = session.query(User).filter(User.id == product_request.user_id).first()
    if user == None:
        return {"message": "user not found"}
    
    product_request = Product(
        user_id=product_request.user_id,
        title=product_request.Product_Title, 
        description=product_request.Product_description, 
        brand_name=product_request.brandName, 
        date_of_manufacture=product_request.dateOfManufacture, 
        color=product_request.color, 
        category=product_request.category
    )
    
    session.add(product_request)
    session.commit()
    session.close()
    return {"status": "success"}