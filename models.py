from sqlalchemy import Column, Integer, TEXT, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(TEXT, nullable=False)
    email = Column(TEXT, nullable=False)
    password = Column(TEXT, nullable=False)
    phonenumber = Column(TEXT, nullable=True)
    # User 모델에서 Product 모델로의 관계를 추가
    product = relationship("Product", back_populates="user")


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(TEXT, nullable=False)
    description = Column(TEXT, nullable=False)
    brand_name = Column(TEXT, nullable=False)
    date_of_manufacture = Column(TEXT, nullable=False)
    color = Column(TEXT, nullable=False)
    category = Column(TEXT, nullable=False)
    # Product 모델에서 User 모델로의 역방향 관계를 정의.
    user = relationship("User", back_populates="product")