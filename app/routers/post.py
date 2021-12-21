from typing import Optional, List
from fastapi import FastAPI, Response, security, status, HTTPException, Depends, APIRouter

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import Session, get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/", response_model=List[schemas.Post]) # List to retrieve more than one post
@router.get("/", response_model=List[schemas.PostOut]) # List to retrieve more than one post
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # Retrieve all posts from database
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    # If it's necessary return only posts of owner
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() -> 
    # current_user need to be pass to function
    print(limit)
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    
    # SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, 
    #   posts.published AS posts_published, posts.created_at AS posts_created_at, posts.owner_id AS posts_owner_id, 
    #   count(votes.post_id) AS votes
    #   FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id GROUP BY posts.id
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).offset(skip).limit(limit).all()
    # print(results)
    
    return posts # automatically serialize data from list


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    # Save post to database    
    # Never use f"" to pass values to database, because SQL Injection
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")
    
    # Sanatize SQL and don't allow SQL Injection
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (
    #     post.title, post.content, post.published))
    # new_post = cursor.fetchone()        
    # conn.commit()
    
    # **post.dict() Para não precisar escrever todos os campos
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Retrieve post and store inside new_post
    
    return new_post
            

# Order matters - if this router come after get_post will retrieve error, because "latest" will be treated as {id}
# @app.get("posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"detail": post}


@router.get("/{id}", response_model=schemas.PostOut) # id: str, to work as id, it's necessary convert to int
def get_post(id: int, response: Response, db: Session = Depends(get_db)):  # It's necessary specify type to fastapi retrieve nice error for frontend if it's not expected type
  
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) # It's necessary convert to string back
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()
        
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found") 
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
       
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()