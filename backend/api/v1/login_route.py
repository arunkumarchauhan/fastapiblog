from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.repository.login import get_user_by_email
from core.security import create_access_token
from core.hashing import Hasher
from db.models.user import User
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from core.config import settings

def authenticate_user(email:str,password:str,db:Session):
    user:User=get_user_by_email(email=email,db=db)
    if not user:
        return False
    if not Hasher.verify_password(password,user.password):
        return False
    return user

router=APIRouter()
@router.post('/token')
def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(OAuth2PasswordRequestForm),db:Session=Depends(get_db)):
    user=authenticate_user(email=form_data.username,password=form_data.password,db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid Credentials')
    access_token=create_access_token(data={'sub':user.email})
    return {'access_token':access_token,'token_type':'bearer'}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token,key=settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception 
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise credentials_exception
    return user
