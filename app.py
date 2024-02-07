from fastapi import FastAPI
from database import Database
from models import Product, User
from pydantic import BaseModel

app = FastAPI()

database = Database()

class ProductRequest(BaseModel):
    user_id: int
    title: str
    description: str
    brand_name: str
    date_of_manufacture: str
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
def create_product(product: ProductRequest):
    session = database.get_session()
    user = session.query(User).filter(User.id == product.user_id).first()
    if user == None:
        return {"message": "user not found"}
    
    product = Product(
        title=product.Product_Title, 
        description=product.Product_description, 
        brand_name=product.brandName, 
        date_of_manufacture=product.dateOfManufacture, 
        color=product.color, 
        category=product.category
    )
    
    session.add(product)
    session.commit()
    session.close()
    return {"status": "success"}