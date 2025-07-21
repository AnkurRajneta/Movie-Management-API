from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config.config import Database



engine = create_engine(Database,connect_args={"check_same_thread" : False}if Database.startswith("sqlite") else {})





SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind = engine)

Base  = declarative_base()




def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()