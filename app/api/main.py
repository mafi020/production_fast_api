from fastapi import APIRouter
from app.api.routers import auth, users, items, ws

# Protected router (auth + rate limiting applied later)
routers = [users.router, items.router]

protected_router = APIRouter(prefix="/api")

for router in routers:
    protected_router.include_router(router)

# Public router (NO auth required)
public_router = APIRouter(prefix="/api")
public_router.include_router(auth.router)
public_router.include_router(ws.router)


# Export both
__all__ = ["public_router", "protected_router"]


    
