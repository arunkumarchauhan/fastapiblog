from db.models.blog import Blog
from sqlalchemy.orm import Session
from schemas.blog import BlogCreate,ShowBlog,UpdateBlog
from fastapi import HTTPException as HttpException,status
def create_new_blog(blog:BlogCreate,db:Session,author_id:int=1):
    new_blog=Blog(title=blog.title,slug=blog.slug,content=blog.content,author_id=author_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_blog(id:int,db:Session):
    blog=db.query(Blog).filter(Blog.id==id).first()
    return blog
def get_all_blogs(db:Session):
    blogs=db.query(Blog).all()
    return blogs
def update_blog(id:int,blog:UpdateBlog,db:Session,author_id:int|None=None):
    existing_blog=get_blog(id=id,db=db)
    if not existing_blog:
        return
    if existing_blog.author_id != author_id:
        raise HttpException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad request! You are not allowed to update this blog")
    existing_blog.title=blog.title
    existing_blog.content=blog.content
    db.add(existing_blog)
    db.commit()
    return existing_blog

def delete_blog(id:int,auth_id:int|None,db:Session):
    blog=get_blog(id=id,db=db)
    if not blog:
        return {"error":f"Could not find blog with id {id}"}
    if blog.author_id != auth_id:
        raise HttpException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad request! You are not allowed to delete this blog")
    db.delete(blog)
    db.commit()
    return {'msg':f'Deleted blog with id {id}'}