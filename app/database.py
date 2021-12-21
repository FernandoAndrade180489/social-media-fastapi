# https://fastapi.tiangolo.com/tutorial/sql-databases/

from sqlalchemy import create_engine, engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# # Try to connect to database  
# while True:  
#     try:
#         conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name, user=settings.database_username, 
#                                 password=settings.database_password, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)