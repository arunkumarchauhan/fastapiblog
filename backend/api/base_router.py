from fastapi import APIRouter
from api.v1 import user_router,login_route,blog_route


api_router=APIRouter()

api_router.include_router(user_router.router,prefix='/user',tags=['user'])
api_router.include_router(blog_route.router,prefix='/blog',tags=['blog'])
api_router.include_router(login_route.router,prefix='',tags=['login'])
