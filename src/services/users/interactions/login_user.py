from services.users.models.user import User
from fastapi.exceptions import HTTPException
from services.users.interactions.create_user_session import create_user_session

def login_user(request):
    user = User.select().where(User.email == request.email)

    if not user:
        raise HTTPException(
            status_code=500, detail="No account exists for the provided email id"
        )

    if not user.verify_password(request.password, user.password_digest):
        raise HTTPException(status_code=500, detail="Incorrect password")

    params = get_session_params(user,request)

    try:
        create_user_session(params)
    except Exception as e:
        return e


def get_session_params(user, request):
    session_payload = {
      "user_id": user.id,
      "auth_scope": request.auth_scope,
      "parent_token": request.parent_token,
      "auth_mode": "password",
    }
    return session_payload

