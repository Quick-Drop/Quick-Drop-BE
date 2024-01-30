# initialize_db.py
from database import Database
from models import Base

def create_tables():
    database = Database()
    Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    create_tables()
