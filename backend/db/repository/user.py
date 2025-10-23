from sqlalchemy.orm import Session,Query
from schemas.user import UserCreate
from db.models.user import User
from core.hashing import Hasher


def create_new_user(user:UserCreate,db:Session):
    new_user=User(email=user.email,password=Hasher.hash_password(user.password),is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

