from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from database import Database
from models import Product, User
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import base64
from PIL import Image
import io
import openai
import env

app = FastAPI()

openai.api_key = env.OPENAI_API_KEY

origins = [
    "http://localhost:58604",
    "http://localhost:3000",  # 필요한 다른 도메인 추가
]

# 애플리케이션 인스턴스에 CORSMiddleware 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # origins 리스트에 나열된 도메인으로부터의 요청을 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

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
    # profile_image_url: str

class UserLocation(BaseModel):
    address: str

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
    image_data: str

class ProductDonated(BaseModel):
    donated: bool

class ImageData(BaseModel):
    data: str

# @app.post("/image/test")
# async def upload_image(image_data: ImageData):
#     try:
#         # base64 문자열을 바이너리 데이터로 디코딩
#         image_bytes = base64.b64decode(image_data.data)
#         # 파일로 저장
#         with open("test.png", "wb") as image_file:
#             image_file.write(image_bytes)
#         return {"message": "Image uploaded successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error saving image: {e}")

@app.get("/")
def read_root():
    return {"message": "GDSC HUFS Quick Drop API Server"}

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
        # 해당 이메일을 가진 사용자가 이미 존재하는지 확인
        user = session.query(User).filter(User.email == user_request.email).first()
        if user != None:
            return {"status": "fail", "message": "user already exists"}
        user = User(
            name=user_request.name,
            email=user_request.email,
            password=user_request.password,
            phone_number="",
            address="",
            profile_image_url=""
        )
        session.add(user)
        session.commit()
        session.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

@app.post("/signin")
# 비동기 방식
async def login_user(login_request: LoginRequest):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.email == login_request.email).first()
        if user == None or user.password != login_request.password:
            return {"status": "fail"}
        session.close()
        return {"status": "success", "user_id": user.id}
    except Exception as e:
        return {"status": "fail", "message": str(e)}
    

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    try:
        session = database.get_session()
        products = session.query(Product).filter(Product.user_id == user_id).all()
        if products == []:
            return {"message": "no products"}
        for product in products:
            session.delete(product)
        session.commit()
        user = session.query(User).filter(User.id == user_id).first()
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
        # user.profile_image_url = user_profile.profile_image_url
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
        return {"address": user.address}
    except Exception as e:
        return {"status": "fail", "message": str(e)}
    
@app.put("/user/{user_id}/location")
def update_user_location(user_id: int, user_location: UserLocation):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return {"message": "user not found"}
        user.address = user_location.address
        session.commit()
        session.close()
        return {"status": "success"}
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
    
@app.get("/user/{user_id}/donations/{status}")
def get_user_donations_by_status(user_id: int, status: bool):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return {"message": "user not found"}
        donations = session.query(Product).filter(Product.user_id == user_id, Product.donated == status).all()
        if donations == []:
            return {"message": "no products"}
        session.close()
        return donations
    except Exception as e:
        return {"status": "fail", "message": str(e)}
    
@app.put("/user/{user_id}/product/{product_id}/donated")
def toggle_donation_status(user_id: int, product_id: int):
    try:
        session = database.get_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user == None:
            return {"message": "user not found"}
        product = session.query(Product).filter(Product.id == product_id).first()
        if product == None:
            return {"message": "product not found"}
        product.donated = not product.donated
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

@app.post("/donation/upload")
async def create_product(product_request: ProductRequest):
    try:
        session = database.get_session()

        user = session.query(User).filter(User.id == product_request.user_id).first()
        if user is None:
            return {"message": "user not found"}
        
        product = Product(
            user_id=product_request.user_id,
            title=product_request.Product_Title, 
            description=product_request.Product_description, 
            brand_name=product_request.brandName, 
            date_of_manufacture=product_request.dateOfManufacture, 
            color=product_request.color, 
            category=product_request.category,
            product_image_data=product_request.image_data  # Base64 인코딩된 이미지 데이터 저장
        )
        session.add(product)
        session.commit()
        session.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}


@app.put("/product/{product_id}/donated")
def update_donation_status(product_id: int, product_donated: ProductDonated):
    try:
        session = database.get_session()
        product = session.query(Product).filter(Product.id == product_id).first()
        if product == None:
            return {"message": "product not found"}
        product.donated = product_donated.donated
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


@app.post("/classify")
async def classify(image_data: ImageData):
    try:
        # Base64 문자열을 바이너리 데이터로 디코딩
        image_bytes = base64.b64decode(image_data.data)
        
        # 이미지 분류 로직 (여기서는 예시로 OpenAI API를 호출한다고 가정)
        result_class = classify_image(image_data.data)  # Base64 인코딩된 데이터를 그대로 넘김
        
        # 분류 결과 반환
        return JSONResponse(content={"result": result_class})
    except Exception as e:
        print(f"Error during classification: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
# 이전 코드
# @app.post("/classify")
# # use desk.png as image_data
# async def classify(file: UploadFile = File(...) ):
#     try:
#         image_data = await file.read()
#         image_data_base64 = base64.b64encode(image_data).decode('utf-8')
#         result_class = classify_image(image_data_base64)
#         return JSONResponse(content={"result": result_class})
#     except Exception as e:
#         print(f"Error during classification: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

