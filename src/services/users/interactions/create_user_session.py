from services.users.models.user_session import UserSession
from services.users.models.user import User
from datetime import datetime, timedelta, timezone
from libs.auth import create_access_token

def create_user_session(request):
    with UserSession._meta.database.atomic():
        return execute_transaction(request)

def execute_transaction(request):
    user = User.select().where(User.id == request.user_id).first()
    access_token_expires = timedelta(minutes=30)
    data = {"sub": user.name, "scopes": []}
    token = create_access_token(data, access_token_expires)
    create_params = get_create_params(request)
    user_session = UserSession(**create_params)
    user_session.token = token
    user_session.save()

def get_create_params(request):
    return request.model_dump(
        include={"user_id", "auth_scope", "status"},
        exclude_none=True,
    )