from app import schemas
from jose import jwt
from app.config import settings
from .database import client, session
import pytest


@pytest.fixture
def test_user(client):
    user_data = {"email": "user@gmail.com", "password": "123456"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


def test_root(client):
    response = client.get("/")
    print(response.json().get("message"))
    assert response.json().get("message") == "Welcome to my api!!"
    assert response.status_code == 200

# "/users/" to work correctly it's necessary have / at the end of URL    
def test_create_user(client):
    res = client.post("/users/", json={"email": "user@gmail.com", "password": "123456"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json()) # Validate if response matchs with Schema fields
    # assert res.json().get("email") == "user@gmail.com"
    assert new_user.email == "user@gmail.com"
    assert res.status_code == 201
    
# Each test need to be independent from others tests    
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']}) # data send as form-data
    print(res.json())
    login_res = schemas.Token(**res.json())
    # Validate access token response
    payload = jwt.decode(login_res.access_token, settings.secret_key , algorithms=[settings.algorithm])        
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200