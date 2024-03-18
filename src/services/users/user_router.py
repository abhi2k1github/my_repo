from fastapi import APIRouter, Query, Depends, Request
from services.users.interactions.create_user import create_user
from services.users.interactions.login_user import login_user
from fastapi.responses import JSONResponse
import sentry_sdk
from fastapi.exceptions import HTTPException
from traceback import format_exc
from fastapi.encoders import jsonable_encoder
from services.users.user_params import CreateUser, LoginUser
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

@user_router.post("/create_user")
def create_user_api(request: CreateUser):
    try:
        data = create_user(request)
        return JSONResponse(status_code=200, content=jsonable_encoder(data))
    except HTTPException as e:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e), "traceback": format_exc()}
        )
    
@user_router.post("/login_user")
def login_user_api(request: LoginUser):
    try:
        data = login_user(request)
        return JSONResponse(status_code=200, content=jsonable_encoder(data))
    except HTTPException as e:
        raise
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e), "traceback": format_exc()}
        )

