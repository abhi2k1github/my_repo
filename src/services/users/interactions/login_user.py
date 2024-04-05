from services.users.models.user import User
from fastapi import status
from fastapi.exceptions import HTTPException
from libs.auth import authenticate_user
from services.users.interactions.create_user_session import create_user_session
from services.users.interactions.get_current_user import get_current_user
from services.users.user_params import LoginUser

def login_user(request: LoginUser):
    user: User = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    params = get_session_params(user,request)

    return create_user_session(params)


def get_session_params(user, request):
    session_payload = {
      "user_id": user.id,
      "auth_scope": request.auth_scope,
      "auth_mode": "password",
      "status": "active"
    }
    return session_payload

