from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.db_support import get_db
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from services.users.user_router import user_router


docs = {
    "title": "MY REPO",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "openapi_url": "/openapi.json",
    "debug": True,
    "swagger_ui_parameters": {"docExpansion": None},
}

app = FastAPI(**docs)

security = HTTPBasic()


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    prefix="/user_service",
    router=user_router,
    tags=["user service"],
    dependencies=[Depends(get_db)],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
