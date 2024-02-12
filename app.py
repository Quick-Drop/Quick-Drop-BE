from fastapi import FastAPI, UploadFile, HTTPException, File
from database import Database
from models import Product, User
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import base64
from PIL import Image
import io
import openai
import env

openai.api_key = env.OPENAI_API_KEY

app = FastAPI()

database = Database()

class UserRequest(BaseModel):
    name: str
    email: str
    password: str

class UserProfile(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str
    profile_image_url: str

class UserLocation(BaseModel):
    location: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ProductRequest(BaseModel):
    user_id: int
    Product_Title: str
    Product_description: str
    brandName: str
    dateOfManufacture: str
    color: str
    category: str

class ProductImage(BaseModel):
    data: str

@app.post("/image/test")
async def upload(item: ProductImage):
    try:
        decoded_data = base64.b64decode(item.data)
        with open("test.png", "wb") as f:
            f.write(decoded_data)
        return {
            "message": "Data received successfully",
            "decoded_data": decoded_data
        }
    except Exception as e:
        return {"message": str(e)}

@app.get("/")
def read_root():
    return {"message": "Hello World"}

######################################## User API ########################################
@app.get("/user")
def get_user():
    session = database.get_session()
    users = session.query(User).all()
    if users == []:
        return {"message": "no data"}
    session.close()
    return users

@app.post("/signup")
def create_user(user_request: UserRequest):
    try:
        session = database.get_session()
        user = User(
            name=user_request.name,
            email=user_request.email,
            password=user_request.password,
        )
        session.add(user)
        session.commit()
        session.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}


@app.post("/signin")
def login_user(login_request: LoginRequest):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.email == login_request.email).first()
        if user == None or user.password != login_request.password:
            return {"status": "fail"}
        session.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return {"message": "user not found"}
        session.delete(user)
        session.commit()
        session.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

@app.get("/user/{user_id}/profile")
def get_user_profile(user_id: int):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return {"message": "user not found"}
        session.close()
        return user
    except Exception as e:
        return {"status": "fail", "message": str(e)}

@app.put("/user/{user_id}/profile")
def update_user_profile(user_id: int, user_profile: UserProfile):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return {"message": "user not found"}
        user.name = user_profile.name
        user.email = user_profile.email
        user.password = user_profile.password
        user.phone_number = user_profile.phone_number
        user.profile_image_url = user_profile.profile_image_url
        session.commit()
        session.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}


######################################## Product API ########################################
@app.get("/product")
def get_product():
    try:
        session = database.get_session()
        example = session.query(Product).all()
        if example == []:
            return {"message": "no data"}
        session.close()
        return example
    except Exception as e:
        return {"status": "fail", "message": str(e)}

@app.get("/user/{user_id}/donations")
def get_user_donations(user_id: int):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return {"message": "user not found"}
        donations = user.product
        if donations == []:
            return {"message": "no products"}
        session.close()
        return donations
    except Exception as e:
        return {"status": "fail", "message": str(e)}

@app.post("/donation/upload")
def create_product(product_request: ProductRequest):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == product_request.user_id).first()
        if user == None:
            return {"message": "user not found"}
        product = Product(
            user_id=product_request.user_id,
            title=product_request.Product_Title, 
            description=product_request.Product_description, 
            brand_name=product_request.brandName, 
            date_of_manufacture=product_request.dateOfManufacture, 
            color=product_request.color, 
            category=product_request.category
        )
        session.add(product)
        session.commit()
        session.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

@app.get("/user/{user_id}/location")
def get_user_location(user_id: int):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return {"message": "user not found"}
        session.close()
        return {"location": user.address}
    except Exception as e:
        return {"status": "fail", "message": str(e)}
    
@app.put("/user/{user_id}/location")
def update_user_location(user_id: int, user_location: UserLocation):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return {"message": "user not found"}
        user.address = user_location.location
        session.commit()
        session.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

######################################## Image Classification API ########################################

classes = ['Utensils', 'Furniture', 'Interior', 'Electronics',
           'Clothes', 'Cosmetics', 'Book', 'Groceries', 'Etc']

def classify_image(image_data_base64):
    try:
        image_data_jpeg = base64.b64decode(image_data_base64)
        image = Image.open(io.BytesIO(image_data_jpeg))
    except Exception as e:
        print(f"Error decoding image: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid image format")

    try:
        with io.BytesIO() as output_buffer:
            image.convert("RGB").save(output_buffer, format="JPEG")
            image_data_jpeg = output_buffer.getvalue()
            image_data_base64 = base64.b64encode(
                image_data_jpeg).decode('utf-8')
    except Exception as e:
        print(f"Error converting image to JPEG: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # GPT에게 이미지를 분석하고 특정 클래스로 답변 요청
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Look at the image and tell me what kind of item it is. Also, let me know which class it belongs to from the following categories: {', '.join(classes)}. The answer is that most images belong somewhere. For example, if the image is 'chair', respond with 'Furniture'. If the image is 'bed', respond with 'Furniture'. If the image is 'hoodie', respond with 'Clothes'.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data_base64}"
                        }
                    }
                ]
            },
            {
                "role": "assistant",
                "content": "I'll do my best to analyze the image and provide you with the appropriate classification.",
            },
            {
                "role": "system",
                "content": "You are a helpful assistant for classifying images.",
            },
        ],
        max_tokens=300,
    )

    # GPT의 답변에서 클래스 추출
    chosen_class = extract_class(response['choices'][0]['message']['content'])

    # 결과 반환
    return chosen_class

def extract_class(content):
    for c in classes:
        if c in content:
            return c
    return None

@app.get("/desk")
def get_desk():
    try:
        with open("desk.png", "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            result_class = classify_image(image_data)
            return JSONResponse(content={"result": result_class})
    except Exception as e:
        return {"status": "fail", "message": str(e)}

@app.post("/classify")
# use desk.png as image_data
async def classify(file: UploadFile = File(...) ):
    try:
        image_data = await file.read()
        image_data_base64 = base64.b64encode(image_data).decode('utf-8')
        result_class = classify_image(image_data_base64)
        return JSONResponse(content={"result": result_class})
    except Exception as e:
        print(f"Error during classification: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    # finally:
    #     cursor.close()
    #     mysql_connection.close()