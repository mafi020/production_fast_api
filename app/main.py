from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

app.include_router(api_router)
