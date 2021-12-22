from fastapi.testclient import TestClient
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
import pytest
from alembic import command

#--------------------------------------- Create Test DataBase-----------------------------------------#
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# # Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # To overrides dependency db: Session = Depends(get_db)        
# app.dependency_overrides[get_db] = override_get_db
#--------------------------------------- Create Test DataBase-----------------------------------------#


# client = TestClient(app)

# With session it's possible have access to database to perfome query
# With scope you can specify when fixture will be executed, defaut is function - each function will executed
# @pytest.fixture(scope="module") # Module will executed once for module scope="module"
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture() 
def client(session):
    # run our code before we run our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db        
    yield TestClient(app)
    # run our code after our test finishes    