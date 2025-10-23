from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.blog import BlogCreate, ShowBlog,UpdateBlog
from db.repository.blog import create_new_blog,get_all_blogs,get_blog,update_blog,delete_blog
from db.models.user import User
from api.v1.login_route import get_current_user

router=APIRouter()

@router.post('/',response_model=ShowBlog,status_code=status.HTTP_201_CREATED)
def create_blog(blog:BlogCreate,db:Session=Depends(get_db),current_user:User=Depends( get_current_user )):
    new_blog = create_new_blog(blog=blog,db=db,author_id=current_user.id)
    return new_blog 

@router.get('/{id}',response_model=ShowBlog,status_code=status.HTTP_200_OK)
def get_blog_by_id(id:int,db:Session=Depends(get_db)):
    blog=get_blog(id=id,db=db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    return blog

@router.get('/',response_model=list[ShowBlog],status_code=status.HTTP_200_OK)
def list_blogs(db:Session=Depends(get_db)):
    blogs=get_all_blogs(db=db)
    return blogs  
    
@router.put('/{id}',response_model=ShowBlog)
def update_by_id(id:int,blog:UpdateBlog,db:Session=Depends(get_db),current_user:User=Depends( get_current_user )):
   
    updated_blog = update_blog(id=id,blog=blog,db=db,author_id=current_user.id)
    if not updated_blog :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'Blog with id {id} does not exist')

    return updated_blog

@router.delete('/{id}')
def delete_a_blog(id:int,db:Session=Depends(get_db),current_user:User=Depends( get_current_user )):
    response=delete_blog(id=id,auth_id=current_user.id,db=db)
    return response
  