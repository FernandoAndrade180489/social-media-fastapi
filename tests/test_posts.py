from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    print(res.json())
    
    def validate_schema(post_out):
        return schemas.PostOut(**post_out)    # Validate if individually post match schema
    posts_map = map(validate_schema, res.json()) # map for validate
    posts_list = list(posts_map)
    print(posts_list)
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 200
    
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200     # If it's necessary login, this should be 401, but it's not necessary
    
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

posts = [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("good news 2022", "the best year come", True),
    ("my pet", "I love my dog", True),    
]

@pytest.mark.parametrize("title, content, published", posts)    
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    
def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "supimpa", "content": "my content"})
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "supimpa"
    assert created_post.content == "my content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']
    
def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title": "supimpa", "content": "my content"})
    assert res.status_code == 401