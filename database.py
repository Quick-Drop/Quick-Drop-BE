from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import env

DB_URL = env.DB_URL

class Database:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle=500)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def get_connection(self):
        return self.engine.connect()
