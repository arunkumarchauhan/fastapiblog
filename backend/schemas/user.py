from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4) # ... means required field

class ShowUser(BaseModel):
    id : int
    email : EmailStr
    is_active : bool
    model_config = ConfigDict(from_attributes=True)
