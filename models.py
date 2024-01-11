from sqlalchemy import Column, Integer, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(TEXT, nullable=False)
    number = Column(Integer, nullable=False)