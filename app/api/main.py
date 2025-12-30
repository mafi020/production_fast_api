from fastapi import APIRouter
from .routers import items, users, auth

api_router = APIRouter(prefix="/api")

routers = [auth.router, users.router, items.router]

for router in routers:
    api_router.include_router(router)
