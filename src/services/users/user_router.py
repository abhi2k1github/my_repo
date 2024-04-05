from fastapi import APIRouter
from services.users.interactions.create_user import create_user
from services.users.interactions.login_user import login_user
from fastapi.responses import JSONResponse
import sentry_sdk
from fastapi.exceptions import HTTPException
from traceback import format_exc
from fastapi.encoders import jsonable_encoder
from services.users.user_params import CreateUser, LoginUser


user_router = APIRouter()

@user_router.post("/create_user")
def create_user_api(request: CreateUser):
    # try:
    data = create_user(request)
    return JSONResponse(status_code=200, content=jsonable_encoder(data))
    # except HTTPException as e:
    #     raise
    # except Exception as e:
    #     sentry_sdk.capture_exception(e)
    #     return JSONResponse(
    #         status_code=500, content={"success": False, "error": str(e), "traceback": format_exc()}
    #     )
    
@user_router.post("/login_user")
def login_user_api(request: LoginUser):
    # try:
    data = login_user(request)
    return JSONResponse(status_code=200, content=jsonable_encoder(data))
    # except HTTPException as e:
    #     raise
    # except Exception as e:
    #     sentry_sdk.capture_exception(e)
    #     return JSONResponse(
    #         status_code=500, content={"success": False, "error": str(e), "traceback": format_exc()}
    #     )

