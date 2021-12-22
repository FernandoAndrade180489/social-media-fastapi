# conftest.py is a special file for tests fixtures. 
# With this file is not necessary import fixtures to test files inside the same packege

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
import pytest
from alembic import command


#--------------------------------------- Create Test DataBase-----------------------------------------#
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#--------------------------------------- Create Test DataBase-----------------------------------------#

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
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # run our code before we run our test        
    yield TestClient(app)
    # run our code after our test finishes    

# fixture to create a user for tests    
@pytest.fixture
def test_user(client):
    user_data = {"email": "user@gmail.com", "password": "123456"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "user2@gmail.com", "password": "123456"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# fixture for create Token for user_test when it's necessary authentication
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

# fixture to generate an authorized client by put token inside header of default client
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']        
    }, {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']        
    }]
    
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                  models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']),
    #                  models.Post(title="3rd title", content="3rdt content", owner_id=test_user['id'])])
    
    session.commit()
    
    return session.query(models.Post).all()


