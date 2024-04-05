from services.users.models.user_session import UserSession
from services.users.models.user import User
from datetime import timedelta, datetime, timezone
from libs.auth import create_access_token

def create_user_session(request):
    with UserSession._meta.database.atomic():
        return execute_transaction(request)

def execute_transaction(request):
    user: User = User.select().where(User.id == request["user_id"]).first()
    access_token_expires = timedelta(minutes=30)
    data = {"sub": str(user.id), "exp": access_token_expires}
    access_token = create_access_token(data, access_token_expires)
    user_session = UserSession(**request)
    user_session.token = access_token
    user_session.expire_at = datetime.now(timezone.utc) + access_token_expires
    user_session.save()
    return {"access_token": access_token, "token_type": "bearer"}