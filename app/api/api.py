from fastapi import APIRouter
from app.api.routers import users_router,ig_router,search


api_router =APIRouter()

api_router.include_router(users_router.router)
api_router.include_router(ig_router.router)
api_router.include_router(search.router)