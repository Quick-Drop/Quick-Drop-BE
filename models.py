from sqlalchemy import Column, Integer, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(TEXT, nullable=False)
    email = Column(TEXT, nullable=False)
    password = Column(TEXT, nullable=False)
    phonenumber = Column(TEXT, nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(TEXT, nullable=False)
    brandName = Column(TEXT, nullable=False)
    dateOfManufacture = Column(TEXT, nullable=False)
    color = Column(TEXT, nullable=False)
    category = Column(TEXT, nullable=False)