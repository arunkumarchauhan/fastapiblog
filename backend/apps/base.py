from apps.v1 import route_blog,route_login
from fastapi import APIRouter

app_route = APIRouter()

app_route.include_router(route_blog.router, prefix="", tags=[""],include_in_schema=False)

app_route.include_router(route_login.router, prefix="/auth", tags=[""],include_in_schema=False)
