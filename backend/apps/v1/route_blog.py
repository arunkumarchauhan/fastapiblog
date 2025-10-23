from fastapi import APIRouter,Request,Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.repository.blog import get_all_blogs,get_blog
from db.session import get_db
templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/")
def home(request: Request,alert:str|None=None,db:Session=Depends(get_db)):
    blogs=get_all_blogs(db=db)
    context = {"request": request, "blogs": blogs,"alert":alert}
    return templates.TemplateResponse("blogs/home.html",context)


@router.get("/app/blog/{id}", name="blog_detail")
def blog_detail(id: int, request: Request, db: Session = Depends(get_db)):
    blog = get_blog(id=id, db=db)
    if not blog:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    context = {"request": request, "blog": blog}
    return templates.TemplateResponse("blogs/detail.html", context)
