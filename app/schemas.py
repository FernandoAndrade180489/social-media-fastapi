from typing import Optional
from pydantic import BaseModel, EmailStr # to use schema for data
from datetime import datetime

from pydantic.types import conint

# Schema for validation using Pydantic module - it's optional, but good pratice

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
# class for response    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
 
    
class PostCreate(PostBase):
    pass


# class for response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # Convert data from database to convert to dict to send back to client
    class Config:
        orm_mode = True
        
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)