from fastapi import APIRouter,Request,Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi import status,Form,responses
from db.repository.user import create_new_user
from schemas.user import UserCreate
from pydantic import ValidationError
from api.v1.login_route import authenticate_user
from core.security import create_access_token

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/register")
def register(request:Request,email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    
    form_data = {'email': email, 'email': email, 'password': password}
    try:
        user_create = UserCreate(**form_data)
        create_new_user(user=user_create, db=db)
        return responses.RedirectResponse(url="/?alert=Successfully%20Registered", status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        errors = e.errors()
        error_messages = [ error['loc'][0] + " : "+error['msg'] for error in errors]
        return templates.TemplateResponse("auth/register.html", {"request": request, "errors": error_messages, "form_data": form_data})
    
@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})   

    
@router.post("/login")
def login(request: Request,email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    user = authenticate_user(email=email, password=password, db=db)
    if user:
        access_token = create_access_token(data={"sub": user.email})
        response = responses.RedirectResponse(url="/?alert=Successfully%20Logged%20In", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response
    else:
        error_message = "Invalid email or password"
        return templates.TemplateResponse("auth/login.html", {"request": request, "errors": [error_message],"email":email,"password":password})
